---
name: session-end
description: Manual lifecycle routine -- session-end (goodnight). Invoke only on an explicit operator request to wrap up; reflection-only by default. Not a conversational helper and not a response to chatter such as "goodnight". Mechanics live in tools/lifecycle.py; the canonical doctrine is doctrine/session-routines.md.
disable-model-invocation: true
---
<!-- cairn-internal-ref-allow: doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Session-end (goodnight)

**Manual only**, and **reflection-only by default.** Run this when an operator
explicitly asks to "wrap up" or "call it a night" -- never from ordinary
conversation ("goodnight, talk tomorrow" is not an instruction to scrub a
roadmap). The canonical doctrine for *what* this routine is and *why* lives in
**`doctrine/session-routines.md`**; this skill only orchestrates it.

## 1. Run the mechanizable step

```
python tools/lifecycle.py session-end $ARGUMENTS
```

`$ARGUMENTS` is whatever follows the command (e.g. `/session-end --handoff`):

* **(no arguments) -- reflection-only, the safe default every agent runs.**
  Scaffolds your per-session reflection file and surfaces open threads; writes
  nothing destructive.
* **`--handoff` -- the full handoff, the designated full-handoff owner only.**
  Preview first (changes nothing): `python tools/lifecycle.py session-end
  --handoff --dry-run`. Then run it with the owner marker:

  ```
  CAIRN_HANDOFF_OWNER=1 python tools/lifecycle.py session-end --handoff
  ```

  The marker is an **anti-accidental-run gate, not an authorization control**;
  a fail-closed lock prevents two concurrent owners from a double roadmap-scrub.
  The CLI runs only the mechanizable steps: prune reflections, metrics, surface
  active intents, and **prune the work-intent log** -- the one step that
  *rewrites* a coordination surface. It removes released claim/release pairs past
  a grace window (default 30d) and never removes an unreleased claim, which it
  reports instead. `dev/modules/coordination-tiers.md` specifies this as the
  goodnight *prune-intents* step; `--handoff --dry-run` lists it before it runs.

## 2. Judgment steps (yours, not the tool's)

**Fill in the reflection** -- what shipped, what went well, what went wrong and
the lesson, what threads stay open -- and migrate any durable observation out to
doctrine or the roadmap before it is pruned. For a full handoff the **roadmap
scrub, the from-scratch next-session rewrite, and the handoff commit** are also
yours.

**Run any project-specific close-out steps** recorded in
`dev/rules/custom_session_routines.md` (the `## Goodnight` section), if present
-- the adopter's concrete routine (doc builds, changelog cadence, test
invocations, foldback capture) lives there, not in this generic skill. A missing
file or a missing section means no custom steps.
