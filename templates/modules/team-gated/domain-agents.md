# Module: domain-agents

**Selected when:** the codebase is **large** — multi-domain, on
the Size axis — *and* the agent team is **multiple**. Size alone
gives partitioned code worked sequentially; this module needs
both.
**Adds to:** the role roster in `dev/agent_collaboration.md`, and
optionally the structure of `dev/PLANNING.md`.

When a large codebase is worked by several agents, the roster
specializes by **domain** rather than by lifecycle stage: each
**Domain Agent** owns the full proposal -> plan -> implement arc
for one domain of the code.

## Template content

Merged into the role roster:

> **Domain Agent.** Each Domain Agent owns one domain of the
> codebase end to end — its proposals, its plans, its
> implementation. Review independence comes from **domain
> rotation**: a change in one domain is reviewed by an agent from
> another, so the reviewer does not share the author's
> domain-specific blind spots.

For a large enough codebase `dev/PLANNING.md` may **shard per
domain**, so each domain's roadmap board stays legible. The
proposal / plan lifecycle itself is unchanged — only the ownership
and the review-independence mechanism specialize.

### Code-bearing cross-domain changes: the Cross-Domain Proposal

A roster that separates a Strategy role (which authors no code-edit
proposals) from per-domain implementers has a structural hole: a
code-bearing change that crosses domains belongs to no single
Domain Agent, and Strategy cannot author the code edit. Such
changes get orphaned — or land without an owner accountable for the
code.

The fix: a **Cross-Domain Proposal** names a **lead Domain Agent** —
the owner of the most-affected domain — plus **co-author Domain
Agents** for the other domains it touches. The lead drives the
proposal → plan → implement arc; the co-authors contribute and
review the parts in their domains. The Strategy role may author the
*non-code* architecture / process framing, but a code-bearing
proposal always has a Domain-Agent owner. Review independence still
comes from domain rotation: the reviewer is an agent from a domain
the change does not touch.

### The ownership ledger — read ownership, don't re-derive it

Prose ownership rules ("Inputs owns preparation; Solver owns the
core") do not scale to a large tree with deep shared categories —
helpers, configuration, UI scaffolding, build glue — that several
domains touch. The first agent to edit a shared file should
**read** ownership off a ledger, not re-derive it from prose each
time. Seed an **ownership ledger**, one row per surface or shared
category:

| Field | What it records |
|---|---|
| surface | the path / module / shared category |
| owning domain | the domain responsible for it |
| shared domains | domains that read or depend on it |
| language | the implementation language |

And **partition shared infrastructure by function, not
wholesale**: rather than declaring "all of the shared directory
belongs to domain X," split it by what each part does — the config
loader to the domain that owns configuration, the plotting helpers
to the domain that owns output — so ownership tracks responsibility
rather than directory accident.
