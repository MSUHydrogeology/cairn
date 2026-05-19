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
