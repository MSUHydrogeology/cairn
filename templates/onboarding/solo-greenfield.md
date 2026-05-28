<!-- Cairn progressive-onboarding task list: solo-greenfield preset.
     Authored under plan 2026-05-28-claude-cairn-progressive-onboarding
     (Chunk P1.1 ships this as a placeholder; Chunk P1.4 fills the
     full task list + active-surfacing prompt content). -->

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
* Active-surfacing prompt metadata blocks (filled in by Chunk
  P1.10b) -- per-row prompt content the activation helper emits
  to the terminal when the row's trigger fires.

## Tasks

* [seed; id: placeholder-solo-greenfield-seed]
  Read `doctrine/lifecycle.md` and open your first proposal as a
  trivial "Hello world"-style accept. (Placeholder content;
  Chunk P1.4 ships the full seed list.)

* [trigger: first-proposal-archived; id: placeholder-solo-greenfield-trigger]
  Walk through `docs/dev-tour.md` to see the rest of the `dev/`
  surfaces. (Placeholder content; Chunk P1.4 fills.)
