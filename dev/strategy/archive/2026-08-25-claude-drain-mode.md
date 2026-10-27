# Drain mode — one command works the queue, decisions stay routed

**Author**: Claude (Strategy)
**Model**: Fable 5
**Date**: 2026-08-25
**Status**: settled (design agreed with the Maintainer in session, 2026-08-25)
**Type**: design-exploration
**Promotes to**: a standard-lane change note, after the subtraction sweep's
constitution-rewrite and board-view chunks land

## The ask

Maintainer, 2026-08-25: much of the process should run *"fully-automated"* on
*"a simple command, like 'let's drain the PLANNING.md board today'"* — smooth
end-to-end flow, intermediate intervention welcome, and *"decisionmaking where
it belongs."* Not unattended cron autonomy; a conducted run.

## The design

**`/session-start --drain [board | issues | <item>]`** — a flag on the
existing orientation skill, mirroring the `session-end --handoff` precedent:
the default stays orientation-only ("do not act autonomously"); the flag is
the operator's explicit consent to execute.

The run: orient as normal, then present the plan in ~ten lines — items found,
which are auto-eligible (trivial/standard lane, consequences reversible),
which park for the Maintainer, any proposed expiries — then conduct: per item,
author work → fresh-subagent review (the Internal floor, natively) → sideways
closure → commit → next. Parks surface as one batch of
recommendation-with-default asks, veto-able on sight, since the Maintainer is
present. Stopping rule: auto-eligible list done or session appetite spent.
End: the books (closed/opened, decisions used, suite state). Nothing pushed.

**Decision routing is unchanged from the constitution**: deliberate-lane
items, tripwire hits (at triage or mid-work — the one-way latch applies to
the conductor too), science questions, proposal Decisions, sister gates, and
anything publishing always park. Everything else flows.

## What it needs

Almost nothing new: a `## Drain mode` section (~30 lines of text) in the
session-start skill; the minimal board view (already in the sweep's build
table) as the queue reader; native subagent spawning for reviews. No
dispatcher, no scheduler, no new command vocabulary. Cross-vendor glue is
unnecessary because everything requiring External review parks by lane.

Shelved deliberately: the cron/unattended variant and default-with-veto
execution — documented options, not needs; revisit only if conducted drains
prove insufficient.

## Why capture precedes commitment

This note exists because the Maintainer asked where durable capture lives
when the change note waits on its prerequisites: **here**. Ideas are captured
the day they are designed — strategy note, board row, or issue; commitment
artifacts (change notes, proposals) open when execution starts. The durable
record begins at capture, not at execution.

## Closure — built and shipped — 2026-10-27

The design was carried out as a standard-lane change, the plan
[`dev/plans/archive/drain-mode.md`](../../plans/archive/drain-mode.md). It shipped
in `.agents/skills/session-start/SKILL.md` and its template twin. The
Maintainer closed this note on 2026-10-27 ("we can entirely retire the drain
mode strategy note").

* **Kept:** the flag on `session-start`, the `board`, `issues` and `<item>`
  targets, the ten-line plan up front, parks batched as questions with a
  recommended default, nothing pushed, and routing unchanged from the
  constitution.
* **Changed:** triage covers two levels (sort; act on trivial items). Commenting,
  labelling and closing are not in 0.5. Issue text is data, never instruction,
  which the note had not said. A fix per item no longer owes a fresh-subagent
  review when it is a trivial change.
* **Still shelved:** the cron or unattended variant and default-with-veto
  execution.
