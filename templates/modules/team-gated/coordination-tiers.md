# Module: coordination-tiers

**Selected when:** the agent team is **concurrent** — more than
one agent in the working tree at once (the Agent-team axis). The
work-intent tier is added for any concurrent team; the typed-event
tier is added only for high-concurrency, domain-agent teams.
**Adds to:** the coordination section of
`dev/agent_collaboration.md`.

The kernel's baseline coordination — path-scoped commits, the
shared-file discipline — catches collisions at *commit* time. This
module adds the higher tiers of the Coordination module, which
give a *pre-edit* signal.

## Template content

Merged into the coordination section:

> **Tier 2 — work intents (concurrent teams).** Before touching a
> collision-prone surface, an agent writes a short, untracked file
> declaring who holds which paths, with what intent and status. It
> is a courtesy signal, not a lock. An empty intent directory
> means "nobody declared", never "nobody is working" —
> version-control state stays the source of truth.
>
> **Tier 3 — typed activity events (high-concurrency teams).** An
> append-only log of typed events — `start`, `heads_up`, `query`,
> `handoff`, `ack`, `release` — a typed channel, not a chat
> channel. The event schema carries no free-form decision field:
> a decision-bearing exchange points an event *at* the proposal or
> plan where the decision is written. The schema is the firewall.

A sequential team runs neither tier — only the kernel's baseline
discipline.
