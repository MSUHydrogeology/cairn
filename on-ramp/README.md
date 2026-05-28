# The on-ramp — graduated adoption

Adopting Cairn is **not** all-or-nothing. There are three levels,
and a project picks the one that fits — the bootstrap recommends a
level from the dimensional profile, but the adopter chooses.

> **Honest framing.** Cairn is **slower for the first few changes**
> at any level: writing decisions down, reviewing them, and
> committing the trail adds friction *before* code. The payback is
> later — fewer repeated decisions, fewer forgotten assumptions,
> fewer agent collisions, and less rework after unreviewed
> scientific choices. Keep the apparatus only as heavy as your
> codebase and team earn; the three levels below are the self-locate
> aid for that calibration.

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

Filling [`../templates/codebase-readiness-report.md`](../templates/codebase-readiness-report.md)
first sharpens the self-locate -- recommended for legacy codebases.
The eleven-section assessment surfaces hidden state, scientific
assumptions, and security boundaries, then maps your G/M/P scores
to a recommended level (≥8 G → Level 2 cleanly; mostly Mixed with
1–2 Poor → Level 1 first; ≥3 Poor → Level 0 while you fix gaps).

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

## The maturity ladder

The ladder is a **self-locate aid, not a scorecard.** It exists so an
adopter can answer "where are we, and what is the next rung?" -- not to
rank teams or score adoptions. (This is the Measurement Compact's
posture: surfaces serve *system learning, not judgment*.) Each rung is
one of the three adoption levels above; "next rung" names the next
deliberate step, which is sometimes *deepening within* a level rather
than jumping to the next.

| Rung | You are here if... | The next rung |
|------|--------------------|---------------|
| **Level 0 — reading the doctrine** | the team reads `doctrine/` and lets it inform how it already works; no `dev/` tree, no templates. | **Level 1**: hand-copy the kernel and run one real change through the lifecycle (see [`../docs/getting-started.md`](../docs/getting-started.md)). |
| **Level 1 — kernel by hand** | the `dev/` tree exists and proposals / reviews / decisions are recorded by hand; the lifecycle runs without the bootstrap script. | *Deepen within Level 1* -- turn on the practice modules the profile warrants (test tiers, the doc-drift gate, an examples gallery) -- **or** move to **Level 2** when the customization is large enough that automating it pays. |
| **Level 2 — bootstrap + improving** | the full bootstrap installed and customized the apparatus, and the team now operates and improves it (Act III). | *Deepen within Level 2* -- adopt governance presets so the module roster is chosen by profile, broaden review tiers, and feed lessons back into the doctrine. There is no rung beyond Level 2; maturity here is depth, not a further level. |

Movement is the adopter's call, informed by the dimensional matrix
(`dimensions/`) -- the ladder shows the path, it does not push.

These levels describe *how much* to adopt. For *how the lifecycle
runs* — one change traced end-to-end — see
[`../docs/getting-started.md`](../docs/getting-started.md), and for
where Cairn sits relative to your build/test/CI tooling,
[`../docs/workflow-role.md`](../docs/workflow-role.md).
