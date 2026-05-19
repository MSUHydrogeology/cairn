# Agent team — single agent ↔ multiple agents

The **agent team** axis is how many AI agents work on the project,
and whether they are of different types. It is the axis that does
the most work: it drives the role roster, the review tiers, and the
coordination tiers. It absorbs what was once a separate
"concurrency" axis — concurrent agents in one working tree is
simply a multi-agent team.

## Scoring rubric

* **Agent count.** One agent, or several?
* **Agent types.** Are the agents the same model architecture, or
  different — and is a human available as an independent reviewer?
* **Concurrency.** Do agents work the tree one at a time, or
  overlapping?
* **Domain specialization.** Are agents general-purpose, or does
  each own a domain of the codebase?

## Positions

### Single agent

One agent wears every role across sessions
(`../doctrine/roles.md`). The review tiers still hold, filled
structurally by *time* rather than by *agent*: Internal review is
the same agent in a fresh session; External review is the
Maintainer, or a second agent type when one becomes available. The
Coordination module runs at its baseline tier only.

### Multiple agents

* **The role roster specializes.** With two agents,
  lifecycle-stage roles — a Strategy agent and an Implementation
  agent — become natural; with many agents and a large codebase,
  domain-specialized agents (`size.md`).
* **The full Dual-Review apparatus is staffable.** A different
  agent type supplies the structural independence the External
  tier wants; review need not collapse onto fresh sessions of one
  agent.
* **Coordination tiers activate.** Concurrent agents in one
  working tree enable the asynchronous tier (work intents); a
  high-concurrency, domain-agent team additionally enables the
  real-time typed-event tier (`../doctrine/coordination.md`).
* On a large domain-agent team, **review independence comes from
  domain rotation** — an agent reviews a domain it does not own.

This axis is where most of Cairn's team-gated apparatus is gated.
A project moving from one agent to two crosses the most
consequential single boundary in the matrix.
