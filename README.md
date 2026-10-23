<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/lifecycle.md doctrine/dual-review.md reason=doctrine/ citation convention — a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Cairn

![Cairn — stacked stones trail-marker logo with project tagline](docs/assets/cairn-banner.svg)

[![DOI](https://zenodo.org/badge/1244751141.svg)](https://doi.org/10.5281/zenodo.23500751)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE-MIT.md)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-blue.svg)](LICENSE-CC-BY.md)
[![Language: Python](https://img.shields.io/badge/Language-Python_3.13-blue.svg)](https://www.python.org/)

Cairn is a working method for scientists developing software with AI coding
agents. It brings together project rules, written proposals, review, testing,
and a record of decisions kept alongside the code.

Research software often outlives the conversation that produced it. Someone
still needs to know why an assumption was made, what a change was checked
against, and what remains uncertain. Cairn gives that information a home in
the repository, so work can continue across sessions, tools, and collaborators.

![Chats end; the repository keeps the record. An agent session today, a different AI tool next week and a new colleague next year all read and write the same files: the project's rules for agents, the proposals recording what was decided and why, the plans recording how it was checked, and the code with its tests.](docs/assets/shared-record-across-sessions.svg)

[Try a small example](docs/quickstart.md) · [See a toy example](#a-toy-example-asking-for-a-new-feature) · [Read the workflow](docs/getting-started.md) · [Browse the methodology](doctrine/) · [Project site](https://msuhydrogeology.github.io/cairn/)

## What it provides

- Project instructions and templates that agents can read and you can edit.
- A way to discuss substantial changes before committing to their implementation.
- Written reviews that question assumptions and check the work against evidence.
- Guidance for testing, documentation, security, and scientific-software practice.
- A versioned record of decisions, unfinished work, and context for the next session.
- Installation and update tools for adapting the method to a particular project.

Cairn is a set of files and local tools, not a hosted development service.
It works with different agent tools and programming languages. You can use
the written guidance on its own or install the templates and supporting tools.

## How the work moves

Not every change needs the same process. Before anything is written, a change
is sorted into one of three lanes, and only the heaviest one carries a proposal
and a plan:

![Three lanes: most changes take a light path. A typo or one-line fix is the change with its test, then a code review. A change whose shape is settled gets a short change note and a review first. Only a new feature, a contract change or a high-risk surface gets a proposal, a review, the Maintainer's decision and a plan. When unsure, take the heavier lane; every step is a commit.](docs/assets/three-lanes-of-change.svg)

For a substantial change, the deliberate lane:

1. Write a proposal explaining the problem, the proposed change, alternatives,
   and what would show it wrong.
2. Have it reviewed while the design can still change.
3. The human Maintainer decides whether to proceed. Non-trivial work gets a
   plan with acceptance criteria.
4. Implement the change and record the checks actually run, including failures
   and omissions. Review the code before closing the work.
5. Keep the proposal, reviews, responses, and decision in git with the code.

Security-sensitive work has additional requirements. The
[lifecycle](doctrine/lifecycle.md) describes how a change is sorted and where
those boundaries sit.

Review is by a fresh reviewer who did not write the work. A fresh session of
the same AI tool is sufficient. The Maintainer can request another model or a
person for a particular review. Each review records who wrote it and the
evidence it considered. The [review guidance](doctrine/dual-review.md) gives
the questions to ask at each stage.

![One review at every stage, by a reviewer who did not write the work and who questions its foundations in writing. A different model or a person adds more distance only when the Maintainer asks, and every review names its reviewer, so that distance is on the record.](docs/assets/dual-review-independence.svg)

The written record is useful in its own right. It lets you revisit a decision,
pick up unfinished work, or understand a scientific assumption without needing
the original chat. It is also work to maintain: if the process obscures the
change or costs more attention than it saves, it needs to be simplified.

## A toy example: asking for a new feature

This is an illustration, not a record from a real project. You ask your agent: *"Check the model's simulated streamflow against the
stream-gauge records, so we can see how well it matches reality."* That is a
new capability, with a new dataset, so it takes the full path. Here is what
happens, and who does it:

| Step | Who | What happens |
| --- | --- | --- |
| **1. Proposal** | The agent, before any code | Writes one short file. **Why:** validation is done by hand in a notebook today, so it is rarely rerun after the model changes. **The change:** read daily discharge records for each gauge, match each gauge to its model stream reach, and report the fit (Nash–Sutcliffe efficiency and percent bias) for each one. **The assumptions, stated:** gauges report cubic feet per second and the model cubic metres per second; missing days are skipped, never treated as zero. **Rejected:** keeping the notebook, because its results cannot be repeated after each change. **How a mistake would show up:** see step 5. |
| **2. Review** | A fresh agent session that did not write it | Asks: *"Gauge records flag days as ice-affected or estimated. Are those compared as if they were measured?"* The author revises: flagged days are left out of the fit, and the report says how many were left out. |
| **3. Decision** | You | Accept, and add one requirement from your own experience: the report also lists the date range each gauge covers, so a short record is never mistaken for a good fit. |
| **4. Plan** | The agent, then a fresh reviewer | Splits the work into steps (reader, matching, statistics, report) with how each will be checked. The reviewer confirms the plan delivers what you accepted, including your added requirement. |
| **5. Build** | The agent | Writes each piece with its tests and documentation. Before trusting the fit statistics on real gauges, it runs them on made-up series whose scores the formulas fix in advance: a series compared with itself must score an efficiency of exactly 1 and a bias of 0, and a flat line at the observed average must score exactly 0. (No real model scores 1; these inputs test the arithmetic, not the model.) A gauge reading of 35.3147 cubic feet per second must arrive as 1.0 cubic metre per second. Then it skips the unit conversion on purpose and records that the check fails, which shows the check can catch that mistake. |
| **6. Code review** | A reviewer who did not build it | Tries to break it with a record that has gaps, a record that starts before the model run, and two gauges on one reach, and records what was tried and what happened. |

Afterwards your repository holds the new code and its tests, plus the proposal,
the review, your decision and the plan, all in git. Next spring, when a
colleague asks *"why are ice-affected days left out of the fit?"*, the answer
is in the review: who raised it, and why. It is a file they can open, not a
chat that has gone.

A small fix skips most of this: a typo or a one-line bug is just the change,
its test and a code review. For real files from a small change, see the
[scientific example](examples/scientific-minimal/), where a reviewer confirms
which test catches a flipped sign in a water-budget formula.

## Engineering practice and scientific judgment

Cairn gives agents a common set of working instructions: test the behavior
being changed, check claims against the files and results, keep changes
reviewable, and ask for a human decision where one is required.

For scientific software, those instructions also need the project's domain
knowledge. A passing test does not establish that a model represents the right
physical process. Units, conservation laws, reference data, numerical tolerances,
and the limits of an interpretation need explicit checks and explanation.

So a change that touches a scientific assumption, such as a governing equation,
a unit or sign convention, a boundary condition or a parameter default, names
one check whose expected answer does not come from the code or from a test
written from the same understanding. The implementer then makes the feared
mistake on purpose and records that the check fails. The
[proposal template](templates/core/dev/proposals/_template.md) sets out what
the check must state.

![A test written from the same understanding as the code can share its mistake: with an outflow sign reversed in both, they agree and the test passes. One check whose expected answer comes from elsewhere, such as an analytical solution, a conservation law aimed at the risk, a trusted observation, an independent implementation or an expert's expectation written down first, disagrees with the code and shows the mistake.](docs/assets/independent-scientific-check.svg)

The [scientific example](examples/scientific-minimal/) shows the workflow around
a mass-balance test. [The rationale](doctrine/rationale.md) explains the research
and experience behind the method, including its limitations.

## Adapt it to your project

A short analysis script and a long-lived simulation model need different amounts
of structure. Cairn uses project profiles and optional modules to choose what
gets installed. Start with the smallest configuration that fits the work.

The installed instructions and templates are ordinary files in your repository.
Some refer to Cairn's published doctrine; your project conventions and local
instructions remain yours to change. Updates use a merge process so local
customizations can be retained, with conflicts resolved explicitly.

See [the on-ramp](on-ramp/README.md) for choosing a profile and
[the glossary](docs/glossary.md) for unfamiliar terms. Useful adaptations can
be proposed back to Cairn.

## Getting started

**Try it on a disposable repository.** The
[quickstart](docs/quickstart.md) walks through one small change with one human
and one agent. The [getting-started guide](docs/getting-started.md) explains
the steps in more detail. [The guides](docs/README.md) map everything else to
read.

Then choose how much to adopt:

- **Read the guidance.** Use [the doctrine](doctrine/) as a handbook without
  installing anything.
- **Install it.** Follow [the bootstrap procedure](bootstrap/BOOTSTRAP.md).
  The Python scaffold installs the files selected by your project profile;
  you and your agent then customize them for the repository.

For an existing scientific codebase, the
[readiness report](templates/codebase-readiness-report.md) helps identify gaps
in tests, data handling, reproducibility, and scientific assumptions before
choosing a configuration.

## Status and limits

Cairn is in active development. The most recent version listed in
[the changelog](CHANGELOG.md) is **0.4.0** (2026-10-20).

Cairn was developed by Anthony Kendall through work on
[modflow_tools](case-studies/modflow_tools.md) and [LHM](case-studies/lhm.md),
and this repository uses the method for its own development. These are
deployments by the same human maintainer, not independent adoptions.

There is no controlled study showing that Cairn improves development outcomes.
An adoption by someone outside its development remains an outstanding test;
no outside project has run the install yet.
The method draws on established practices, but its benefits and costs need
to be judged in use. [Related practices](docs/related-practices.md) describes
the overlap with decision records, lab notebooks, pre-registration, and code
review.

## Safety

AI coding agents can read files, run commands, and send repository content to
their model provider. Keep secrets, credentials, private paths, embargoed
datasets, and unpublished results out of agent-readable material. Check the
permissions and data-handling terms of the agent you use.

Cairn's scanners and integrity checks have limits; a clean result is not proof
that a file or operation is safe. Read [the security statement](SECURITY.md)
before installing third-party instructions or running agents on sensitive work.

## Repository guide

| Directory | Contents |
| --- | --- |
| [doctrine/](doctrine/) | The methodology: decisions, review, roles, session continuity, and rationale. |
| [templates/](templates/) | Instructions, document templates, and optional modules installed into a project. |
| [dimensions/](dimensions/) | How the configuration varies with the codebase and team. |
| [bootstrap/](bootstrap/) | Installation, upgrades, integrity checks, and their tests. |
| [docs/](docs/README.md) | Start here: a map of the guides. |
| [examples/](examples/) | Small repositories showing the workflow. |
| [case-studies/](case-studies/) | Accounts of using Cairn in research-software projects. |
| [dev/](dev/) | Cairn's own proposals, plans, strategy, and development record. |

## License and citation

Source code is [MIT licensed](LICENSE-MIT.md), wherever it lives. Prose,
document templates, and explanatory diagrams are
[CC BY 4.0](LICENSE-CC-BY.md). The Cairn brand mark alone is
[CC BY-ND 4.0](LICENSE-CC-BY-ND.md).

If you use Cairn, see [CITATION.cff](CITATION.cff) for citation details.
Cite using the DOI ([10.5281/zenodo.23500751](https://doi.org/10.5281/zenodo.23500751)) or the version and repository URL.
