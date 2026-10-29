# Contributing to Cairn

Thank you for considering a contribution. Cairn is an open-science methodology
for research-software teams using AI coding agents. It is built and maintained
in the open, and contributions should leave a clear record that another reader
can understand and review.

## Before you start

For a bug or a small correction, open an issue with what you observed and how
to reproduce it, or use the matching issue form. For a substantial change,
start with a proposal in the repository's `dev/` process before implementing
it. That gives contributors and maintainers a chance to agree on the problem,
design, and evidence while the change is still easy to shape. The project's
`AGENTS.md` and `dev/` guides describe the shared workflow.

If you are unsure which path fits, open an issue to discuss it before doing
substantial work. Please do not include secrets, credentials, private paths,
embargoed data, or unpublished results in an issue or pull request; repository
issues and pull requests are public.

## Preparing a change

Read [`AGENTS.md`](AGENTS.md) for the development environment, project
conventions, verification commands, and commit workflow. For the proposal,
review, and plan process, begin with [`dev/README.md`](dev/README.md) and
[`dev/agent_collaboration.md`](dev/agent_collaboration.md). Use the repository's
existing templates and checks, and keep the change focused on the agreed work.

Before opening a pull request:

* Run the checks that apply to the files you changed, following `AGENTS.md`.
* Record the commands and results, including any known gaps.
* Make sure the change and its evidence are committed.

## Opening a pull request

Use the pull request template and explain the problem, the change, and how you
checked it. Link the related issue or deliberation record when there is one.
Reviewers may ask for changes or a different approach; discuss concerns in the
pull request so the reasoning stays with the work.

## Project structure

The [README](README.md) introduces Cairn, and [`docs/README.md`](docs/README.md)
maps its user documentation. The `doctrine/` directory contains the published
methodology; `templates/` and `bootstrap/` contain the materials and tools that
adopters use. Development records live under `dev/`.
