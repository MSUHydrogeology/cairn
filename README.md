<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/lifecycle.md doctrine/dual-review.md reason=doctrine/ citation convention — a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Cairn

![Cairn — stacked stones trail-marker logo with project tagline](docs/assets/cairn-banner.svg)

Cairn is a working method for scientists developing software with AI coding
agents. It brings together project rules, written proposals, review, testing,
and a record of decisions kept alongside the code.

[![DOI](https://zenodo.org/badge/1244751141.svg)](https://doi.org/10.5281/zenodo.23500751)

Research software often outlives the conversation that produced it. Someone
still needs to know why an assumption was made, what a change was checked
against, and what remains uncertain. Cairn gives that information a home in
the repository, so work can continue across sessions, tools, and collaborators.

[Try a small example](docs/quickstart.md) · [Read the workflow](docs/getting-started.md) · [Browse the methodology](doctrine/)

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

For a substantial change:

1. Write a proposal explaining the problem, the proposed change, alternatives,
   and what would show it wrong.
2. Have it reviewed while the design can still change.
3. The human Maintainer decides whether to proceed. Non-trivial work gets a
   plan with acceptance criteria.
4. Implement the change and record the checks actually run, including failures
   and omissions. Review the code before closing the work.
5. Keep the proposal, reviews, responses, and decision in git with the code.

Small, routine edits take a lighter path; security-sensitive work has additional
requirements. The [lifecycle](doctrine/lifecycle.md) describes those boundaries.

Review is by a fresh reviewer who did not write the work. A fresh session of
the same AI tool is sufficient. The Maintainer can request another model or a
person for a particular review. Each review records who wrote it and the
evidence it considered. The [review guidance](doctrine/dual-review.md) gives
the questions to ask at each stage.

The written record is useful in its own right. It lets you revisit a decision,
pick up unfinished work, or understand a scientific assumption without needing
the original chat. It is also work to maintain: if the process obscures the
change or costs more attention than it saves, it needs to be simplified.

## Engineering practice and scientific judgment

Cairn gives agents a common set of working instructions: test the behavior
being changed, check claims against the files and results, keep changes
reviewable, and ask for a human decision where one is required.

For scientific software, those instructions also need the project's domain
knowledge. A passing test does not establish that a model represents the right
physical process. Units, conservation laws, reference data, numerical tolerances,
and the limits of an interpretation need explicit checks and explanation.

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
Until a DOI is issued, cite the version and repository URL.
