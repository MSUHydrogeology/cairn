# Size — small ↔ large

A codebase's **size** is how much code there is and how many
distinct domains it spans. Size drives whether the *code* — and
the roadmap that tracks it — is partitioned into domains. How the
*agent roster* specializes is a related but separate question (see
`agent-team.md`); Cairn keeps codebase size and team size on
independent axes, because they vary independently.

## Scoring rubric

* **Line and module count.** A rough magnitude — thousands of
  lines and a handful of modules, versus hundreds of thousands and
  many.
* **Distinct domains.** How many genuinely separate areas of
  concern does the code span — and do they have different
  vocabularies, different contributors, different change rhythms?
* **Public-API surface.** A large public surface is itself a kind
  of size: more contracts to hold stable.
* **Roadmap legibility.** Can one roadmap board still be read at a
  glance, or has it grown into a board nobody reads whole?

## Positions

### Small

One unpartitioned codebase. A single roadmap board tracks all
work; a contributor holds the whole structure in mind. No domain
partitioning.

### Large

The code spans several domains, and that has consequences:

* The **code** is partitioned into domains with explicit
  boundaries between them.
* The roadmap board may **shard per domain**, so each domain's
  board stays legible.
* Large size *enables* a domain-specialized agent roster — but it
  does not by itself *create* one; that needs a multi-agent team
  (`agent-team.md`). A large codebase with a solo team is
  partitioned code worked sequentially.

The signal that a codebase has crossed into "large" is not a line
count but a legibility loss: when no single board, and no single
contributor's mental model, covers the whole anymore.
