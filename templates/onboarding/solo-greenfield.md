<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/lifecycle.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Cairn progressive-onboarding task list: solo-greenfield preset.
     Authored under plan 2026-05-28-claude-cairn-progressive-onboarding
     (Chunk P1.4 fills the full task list + active-surfacing prompt
     content; P1.1 shipped a placeholder ahead of this). -->

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
  when the row's trigger fires.

The `solo-greenfield` preset assumes the lightest shape: one
human Maintainer + one AI agent on a new or near-new codebase.
The tasks are calibrated for that scale -- no team negotiation,
no multi-agent coordination, no legacy-tree pre-pass.

## Tasks

* [seed; id: try-session-start-skill]
  Try the `session-start` skill (`/session-start`): run
  `python tools/session.py session-start` to orient at the top of a
  session. The lifecycle routines are now invokable skills installed under
  `.agents/skills/`; the canonical doctrine is `doctrine/session-routines.md`.

* [seed; id: read-lifecycle-doctrine]
  Read `doctrine/lifecycle.md`. It is the single load-bearing
  read for every Cairn deployment; the rest of the apparatus
  makes more sense after.

* [seed; id: skim-coordination-doctrine]
  Skim `doctrine/coordination.md`. The work-intent mechanism
  earns its keep when you add a second agent; for solo-greenfield
  you can defer the deeper read until that day comes.

* [seed; id: walk-dev-tour]
  Walk the `dev/`-tree tour at `dev/modules/onboarding/dev-tour.md`.
  It carries one paragraph per `dev/` subdirectory plus a worked example
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

* [trigger: second-agent-type; id: spin-up-second-agent]
  You're at the point where a second agent type would be useful.
  Fresh sessions of your agent already do every review, and you can
  read any piece of work yourself; a second agent type makes a
  different model's read available whenever you ask for one, and
  eases how much falls on you alone. Walk
  `dev/modules/onboarding/agent-team-onboarding.md` for the spin-up
  checklist.

* [seed; id: walk-foldback-protocol]
  The fold-back practice: when you improve the method itself, not
  just your project, that improvement belongs upstream. This is
  your introduction to the fold-back issue template
  (`.github/ISSUE_TEMPLATE/foldback.md`); it walks you through
  filing your first upstream Cairn issue or PR.

## Active-surfacing prompt content (per-preset)

Each active-surfacing row carries per-preset prompt content that
the activation helper emits to the terminal when the row's
trigger fires. The `solo-greenfield` shape has one row:

### Row 1 -- second-agent-type spin-up prompt

Your solo deployment has matured to a point where a second agent
type would be useful. Fresh sessions of your agent already do every
review, and you can read any piece of work yourself; a second agent
type makes a different model's read available whenever you ask for
one, and eases how much falls on you alone. Walk
`dev/modules/onboarding/agent-team-onboarding.md` for the spin-up
checklist; the second agent's capability tier should match the
work it will do.
