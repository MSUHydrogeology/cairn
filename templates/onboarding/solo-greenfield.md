<!-- Cairn progressive-onboarding task list: solo-greenfield preset.
     Authored under plan 2026-05-28-claude-cairn-progressive-onboarding
     (Chunk P1.4 fills the full task list + active-surfacing prompt
     content; P1.1 shipped a placeholder ahead of this). -->
<!-- claim-check-allow: docs/agent-team-onboarding.md -->
<!-- The agent-team-onboarding.md reference resolves when Chunk
     P1.7 ships `cairn/docs/agent-team-onboarding.md`. -->

# Onboarding tasks -- solo-greenfield

This file ships **three kinds of content**, segregated by tag
syntax so the scaffold + the activation helper can parse them
unambiguously:

* `[seed; id: <name>]` lines -- day-one PLANNING entries.
  Inlined into `dev/PLANNING.md`'s `onboarding-tasks` slot at
  scaffold install time.
* `[trigger: <trigger-name>; id: <name>]` lines -- held in this
  source file; activated into PLANNING when the named trigger
  fires (the goodnight `onboarding_activate.py` helper does the
  matching).
* Active-surfacing prompt metadata blocks at the end -- per-row
  prompt content the activation helper emits to the terminal
  when the row's trigger fires (the four named rows; P1.10b fills
  per-preset prompt content).

The `solo-greenfield` preset assumes the lightest shape: one
human Maintainer + one AI agent on a new or near-new codebase.
The tasks are calibrated for that scale -- no team negotiation,
no multi-agent coordination, no legacy-tree pre-pass.

## Tasks

* [seed; id: read-lifecycle-doctrine]
  Read `doctrine/lifecycle.md`. It is the single load-bearing
  read for every Cairn deployment; the rest of the apparatus
  makes more sense after.

* [seed; id: skim-coordination-doctrine]
  Skim `doctrine/coordination.md`. The work-intent mechanism
  earns its keep when you add a second agent; for solo-greenfield
  you can defer the deeper read until that day comes.

* [seed; id: walk-dev-tour]
  Walk the `dev/`-tree tour at `docs/dev-tour.md`. It carries
  one paragraph per `dev/` subdirectory plus a worked example
  showing a single trivial change through the full
  proposal -> review -> decision -> archive lifecycle.

* [seed; id: open-first-proposal]
  Open your first proposal -- a "Hello world"-style trivial
  accept -- following the lifecycle the dev-tour just walked.
  This is the single best way to learn the apparatus by doing.

* [trigger: first-proposal-archived; id: post-first-proposal]
  Now that you've shipped one change end-to-end, the
  rest of the dev-tree is the next surface to explore:
  `strategy/` (long-horizon framing docs that aren't yet
  proposals) and `reflections/` (the daily handoff channel) carry
  deliberation surfaces beyond the proposal / plan lifecycle.

* [trigger: collab-agreement-signing; id: sign-collab-agreement]
  Your deployment has accreted enough activity to warrant
  signing the collaboration agreement. Fill the `team-roster`
  slot in `dev/collaboration_agreement.md` with your name + your
  agent's identifier. No multi-party negotiation needed --
  you're the team -- but the explicit roster matters for the
  cross-agent-type review tier when you add a second agent later.

* [trigger: second-agent-type; id: spin-up-second-agent]
  You're at the point where a second agent type meaningfully
  strengthens Dual-Review's External tier (currently filled by
  fresh-session same-vendor review). Walk
  `docs/agent-team-onboarding.md` for the spin-up checklist.

* [trigger: first-foldback-candidate; id: walk-foldback-protocol]
  Your fold-back ledger has its first open candidate ready to
  surface upstream. This is your introduction to the foldback
  active-surfacing protocol (`doctrine/fold-back.md > Active
  surfacing`); it walks you through filing your first upstream
  Cairn issue or PR.

## Active-surfacing prompt content (per-preset)

Per Codex External Review P2-3 + plan P1.10b: each active-surfacing
row carries per-preset prompt content the activation helper emits
to the terminal when the row's trigger fires. The four rows for
the `solo-greenfield` shape:

### Row 1 -- collab-agreement-signing prompt

Fill in your own name + your agent's identifier in the team-roster
slot of `dev/collaboration_agreement.md`. No multi-party
negotiation needed; you're the team. The roster makes the
fresh-session External review tier reproducible (the second
session of your agent reviewing your work is structurally
independent only if the roster names you both explicitly).

### Row 2 -- Level 1→2 graduation prompt

Your deployment has accreted enough lifecycle activity
(proposals + plans archived) that Level 2's bootstrap-managed
lifecycle becomes net-positive vs. by-hand operation. Walk
`bootstrap/BOOTSTRAP.md` -- the bootstrap can re-scaffold your
existing tree non-destructively. No urgency: Level 1 keeps
working; Level 2 just automates what's now repeated work.

### Row 3 -- second-agent-type spin-up prompt

Your solo deployment has matured to a point where a second agent
type would meaningfully strengthen Dual-Review's External tier
(currently filled by fresh-session same-vendor review). Walk
`docs/agent-team-onboarding.md` for the spin-up checklist; the
second agent's capability tier should match the work the
External tier carries.

### Row 4 -- upstream PR/issue walkthrough prompt

Your fold-back ledger now carries a candidate ready to surface
upstream. This is your first introduction to the foldback active-
surfacing prompt (`doctrine/fold-back.md > Active surfacing`) --
it walks you through filing a Cairn issue or PR.
