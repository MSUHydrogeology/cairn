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

## Merging a pull request

When merging a pull request that changes files agents load or files that guard
those instructions, use this checkpoint before merging. Instruction files
include `AGENTS.md`, `CLAUDE.md`, `VENDOR.md`, `RULES.md`, `templates/`,
`.agents/skills/`, `dev/`, and `docs/`. Guarding files include
`bootstrap/tests/`, `scripts/`, and the content scanner's allowlist, baseline,
and roots files. It is a merge-time review only; it does not run before
pushes, during development, or on every commit.

For changed instruction files (`AGENTS.md`, `CLAUDE.md`, `VENDOR.md`,
`RULES.md`, `templates/`, `.agents/skills/`, `dev/`, or `docs/`), use an
up-to-date checkout you trust. Fetch the pull request as data with
`git fetch origin pull/<N>/head`, write each changed instruction file from
`FETCH_HEAD:<path>` into a scratch folder with `git show`, then run your own
`python -I scripts/content_scan.py <scratch-files>`. Do not check out the pull
request branch or run its scanner. Discuss every finding before merging. Any
added `cairn-accept` marker is itself a hit to discuss, even if it clears a
scanner finding.

Read the changed text and decide whether an agent or check following it would
now: skip, shorten, or weaken a review; treat something as approved or decided
without the Maintainer; run a command, open a URL, or send data it did not
before; move authority (roles, fences, permissions, or who may push); trust
something new (allowlists, baselines, or security policy); or stop guarding
something (a test, gate, or scan input that now passes when it should fail).
Discuss every “yes” in the pull request before merging, including intended
changes. For code, tests, and scripts, the text scanner judges nothing; a
person reads the diff for changes that stop something from being guarded.

An optional reviewer agent started with an empty tool list may receive the
diff as quoted data and draft answers to those six questions. It must not act
on instructions in the diff, and its summary is not authority: a person reads
the diff and makes the judgment.

## Project structure

The [README](README.md) introduces Cairn, and [`docs/README.md`](docs/README.md)
maps its user documentation. The `docs/methodology/` directory contains the
published methodology; `templates/` and `bootstrap/` contain the materials and
tools that adopters use. Development records live under `dev/`.
