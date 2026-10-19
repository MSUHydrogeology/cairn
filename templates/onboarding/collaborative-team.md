<!-- cairn-internal-ref-allow: doctrine/coordination.md doctrine/lifecycle.md doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- Cairn progressive-onboarding task list: collaborative-team preset.
     Authored under plan 2026-05-28-claude-cairn-progressive-onboarding
     (Chunk P1.5 fills the full multi-agent + multi-human task list;
     P1.1 shipped a placeholder ahead of this). -->

# Onboarding tasks -- collaborative-team

This file ships **three kinds of content**, segregated by tag
syntax so the scaffold + the activation helper can parse them
unambiguously:

* `[seed; id: <name>]` lines -- day-one PLANNING entries.
* `[trigger: <trigger-name>; id: <name>]` lines -- held until the
  named trigger fires.
* Active-surfacing prompt content blocks at the end -- per-row
  prompt content emitted to the terminal when the row's trigger
  fires.

The `collaborative-team` preset assumes a richer shape than
solo-greenfield: 2-4 humans + 1-2 agent types on a greenfield or
near-greenfield codebase. The tasks are calibrated for that scale
-- team coordination matters from day one; the second agent type
is part of the expected baseline, not a future upgrade; a team
this size has the standing capacity to notice and file fold-back
candidates upstream early, rather than letting the practice lapse.

## Tasks

* [seed; id: try-session-start-skill]
  Try the `session-start` skill (`/session-start`): run
  `python tools/session.py session-start` to orient at the top of a
  session. The lifecycle routines are now invokable skills installed under
  `.agents/skills/`; the canonical doctrine is `doctrine/session-routines.md`.

* [seed; id: read-lifecycle-doctrine]
  Read `doctrine/lifecycle.md` together as a team -- the
  proposal -> review -> decision -> archive shape is the load-
  bearing convention every later coordination behavior assumes.

<!-- cairn:if agent_team in concurrent-multi-type,concurrent-single-type -->
* [seed; id: read-coordination-doctrine]
  Read `doctrine/coordination.md`. The work-intent mechanism is
  what prevents collision between concurrent agents in the same
  tree; multi-agent teams need this from day one, not as a
  later upgrade.

* [seed; id: install-work-intent-hooks]
  Install the work-intent git hooks, or record that you are skipping
  them. This preset is concurrent, so the scaffold *recommended* the
  hooks at install time but does **not** install them for you (it
  never mutates `.git/hooks`). Run `python tools/intent.py
  install-hook` + `install-precommit`, then `hooks-status` to confirm.
  Without them, `dev/intents.jsonl` stays empty and the coordination
  signal never fires. To opt out (now or later), re-run either command
  with `--uninstall`; note the choice here so the team's preference is
  on the record.
<!-- cairn:endif -->

<!-- cairn:if agent_team in concurrent-multi-type -->
* [seed; id: read-dual-review-module]
  Read `dev/modules/dual-review.md`. The collaborative-team
  preset installs the dual-review module by default; it carries
  the guidance for staffing a read the Maintainer calls from a
  different agent type, which this team can now staff.
<!-- cairn:endif -->

* [seed; id: walk-dev-tour]
  Walk the `dev/`-tree tour at `dev/modules/onboarding/dev-tour.md`
  together. It carries one paragraph per `dev/` subdirectory plus a
  worked example showing one change through the full lifecycle.

<!-- cairn:if agent_team in concurrent-multi-type -->
* [seed; id: agent-team-onboarding]
  Walk `dev/modules/onboarding/agent-team-onboarding.md` to align on capability
  tiers + the `Co-Authored-By:` trailer convention for each
  agent in the roster. Multi-agent is this preset's defining
  shape; the agent-team-onboarding doc carries the
  baseline configuration the team uses.
<!-- cairn:endif -->

* [seed; id: fill-team-roster-day-one]
  Convene the team + agents in your first session and fill the
  `team-roster` slot in `dev/agent_collaboration.md`. The
  roster records who is who, so every review names its
  reviewer and a read the Maintainer calls from a different
  agent type can be staffed; a team without an explicit roster
  has reviews no one can attribute, which the
  collaborative-team profile is sized past.

* [trigger: first-proposal-archived; id: post-first-proposal-team]
  Now that the team has shipped one change end-to-end, the
  `strategy/` and `reflections/` channels are the next surfaces
  to staff. Reflections are gitignored by default but the team
  may keep them tracked if cross-agent handoff is intensive.

* [trigger: first-cross-type-review; id: post-first-cross-type]
  Your first cross-agent-type review just shipped. That's the
  distance a different agent type brings, recorded in the file.
  Ask for it again when you want more distance on a piece of
  work; a fresh session remains the usual review.

* [seed; id: walk-foldback-protocol]
  The fold-back practice: when the team improves the method
  itself, not just this project, that improvement belongs
  upstream. Notice it, then file a Cairn issue with the fold-back
  issue template (`.github/ISSUE_TEMPLATE/foldback.md`); the
  team-handoff owner files, coordinating with the team first to
  avoid duplicate Cairn issues.

## Active-surfacing prompt content (per-preset)

The active-surfacing row the collaborative-team preset emits:

### Row 1 -- second-agent-type spin-up prompt

Your collaborative-team profile expects multi-agent operation;
the second agent type makes a more distant read available whenever
the Maintainer asks for one. Walk
`dev/modules/onboarding/agent-team-onboarding.md`; the team's existing roster +
intent-claim discipline already cover the coordination
preconditions, so spin-up is faster than a fresh start.
