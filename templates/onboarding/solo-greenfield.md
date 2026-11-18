<!-- Cairn onboarding task list: solo-greenfield preset. -->

# Onboarding tasks -- solo-greenfield

This file ships **one kind of content**: `[seed; id: <name>]`
lines, the day-one PLANNING entries. The scaffold inlines them into
`dev/PLANNING.md`'s `onboarding-tasks` slot at install time, and
nothing reads this file afterward.

The `solo-greenfield` preset assumes the lightest shape: one
human Maintainer + one AI agent on a new or near-new codebase.
The tasks are calibrated for that scale -- no team negotiation,
no multi-agent coordination, no legacy-tree pre-pass.

## Tasks

* [seed; id: write-style-guide]
  Set conventions as the first code is written. Write a human style guide in the descriptive docs and a short,
  actionable agent version in project-owned rules, routed from `RULES.md`
  (or in `AGENTS.md` project conventions if no router exists). Add a note to
  keep them aligned; optional preferences may drift. Binding rules and higher
  security, dependency and license duties govern decisions. Report conflicts
  and propose correction. If `modules/documentation-plan.md` exists relative
  to this board, see its Style guide section and use the installed documentation
  plan to choose the human guide's home.

* [seed; id: try-session-start-skill]
  Try the `session-start` skill (`/session-start`): run
  `python dev/tools/session.py session-start` to orient at the top of a
  session. The lifecycle routines are now invokable skills installed under
  `.agents/skills/`; the canonical doctrine is `docs/methodology/session-routines.md`.

* [seed; id: read-lifecycle-doctrine]
  Read `docs/methodology/lifecycle.md`. It is the single load-bearing
  read for every Cairn deployment; the rest of the apparatus
  makes more sense after.

* [seed; id: skim-coordination-doctrine]
  Skim `docs/methodology/coordination.md`. The work-intent mechanism
  earns its keep when you add a second agent; for solo-greenfield
  you can defer the deeper read until that day comes. When you add a
  second agent type, walk
  `dev/modules/onboarding/agent-team-onboarding.md`.

* [seed; id: walk-dev-tour]
  Walk the `dev/`-tree tour at `dev/modules/onboarding/dev-tour.md`.
  It carries one paragraph per `dev/` subdirectory plus a worked example
  showing a single trivial change through the full
  proposal -> review -> decision -> archive lifecycle.

* [seed; id: open-first-proposal]
  Open your first proposal -- a "Hello world"-style trivial
  accept -- following the lifecycle the dev-tour just walked.
  This is the single best way to learn the apparatus by doing.

* [seed; id: walk-foldback-protocol]
  The fold-back practice: when you improve the method itself, not
  just your project, that improvement belongs upstream. This is
  your introduction to the installed fold-back template and publication
  protocol (`dev/upstream/foldback.md`); follow it when preparing an upstream
  Cairn issue or PR.
