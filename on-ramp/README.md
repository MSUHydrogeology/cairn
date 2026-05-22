# The on-ramp — graduated adoption

Adopting Cairn is **not** all-or-nothing. There are three levels,
and a project picks the one that fits — the bootstrap recommends a
level from the dimensional profile, but the adopter chooses.

## Level 0 — read the doctrine

Adopt nothing mechanically. Read `doctrine/` as a handbook and let
it inform how the team already works — no `dev/` tree, no
templates. This is the lowest-commitment entry: the project takes
the *ideas* (recorded deliberation, the Dual-Review model) without
the apparatus. The Turing Way is the model for this mode.

## Level 1 — hand-copy the kernel

Copy the invariant-kernel templates (`templates/core/`) into the
repository, add the modules the dimensional profile selects, and
run the lifecycle by hand: write proposals, review them, record
decisions, keep the `dev/` tree. No bootstrap script — the adopter
fills the placeholders themselves. Best for a small, simple
project that wants the discipline without the machinery.

## Level 2 — run the bootstrap

Run the full bootstrap (`bootstrap/`): an agent assesses the
project (Act I), installs and customizes the apparatus (Act II),
and the team then operates and improves it (Act III). Best for a
large, legacy, or multi-team project, where the customization is
substantial enough that automating it pays.

## Choosing a level

| The project is... | Start at |
|-------------------|----------|
| exploring the ideas, not yet committed | Level 0 |
| small, simple, one or two contributors | Level 1 |
| large, legacy, or multi-team | Level 2 |

The levels are an **on-ramp, not a fork**: a project can move up.
Level 0 readers become Level 1 adopters; a Level 1 project runs
the bootstrap later to formalize what it assembled by hand. The
dimensional matrix (`dimensions/`) informs the recommendation, but
the choice is always the adopter's.

These levels describe *how much* to adopt. For *how the lifecycle
runs* — one change traced end-to-end — see
[`../docs/getting-started.md`](../docs/getting-started.md), and for
where Cairn sits relative to your build/test/CI tooling,
[`../docs/workflow-role.md`](../docs/workflow-role.md).
