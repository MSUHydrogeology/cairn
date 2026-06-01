---
name: session-end
description: Manual lifecycle routine -- session-end (goodnight). Invoke only on an explicit operator request to wrap up; reflection-only by default. Not a conversational helper and not a response to chatter such as "goodnight". Mechanics live in tools/lifecycle.py; the canonical doctrine is doctrine/session-routines.md.
disable-model-invocation: true
---

# Session-end (goodnight)

**Manual only**, and **reflection-only by default.** Run this when an operator
explicitly asks to "wrap up" or "call it a night" -- never from ordinary
conversation ("goodnight, talk tomorrow" is not an instruction to scrub a
roadmap). The canonical doctrine for *what* this routine is and *why* lives in
**`doctrine/session-routines.md`**; this skill only orchestrates it.

## 1. Reflection-only (every agent -- the safe default)

```
python tools/lifecycle.py session-end
```

Scaffolds your per-agent reflection file and surfaces open threads; it writes
nothing destructive. Then **fill in the reflection** (judgment): what shipped,
what went well, what went wrong and the lesson, what threads stay open. Migrate
any durable observation out to doctrine or the roadmap before it is pruned.

## 2. Full handoff (the designated owner only)

Only the single agent the maintainer designates as full-handoff owner runs the
guarded path. Preview it first -- this changes nothing:

```
python tools/lifecycle.py session-end --handoff --dry-run
```

Then, as the designated owner:

```
CAIRN_HANDOFF_OWNER=1 python tools/lifecycle.py session-end --handoff
```

The marker is an **anti-accidental-run gate, not an authorization control**; a
fail-closed lock prevents two concurrent owners from a double roadmap-scrub. The
CLI runs the mechanizable steps (prune reflections, metrics, intent surface).
The roadmap scrub, the from-scratch next-session rewrite, and the handoff commit
remain **your** judgment steps.

Friendly alias: `/goodnight`.
