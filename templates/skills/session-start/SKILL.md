---
name: session-start
description: Manual lifecycle routine -- session-start (good-morning) orientation. Invoke only on an explicit operator request to orient / catch up; not a conversational helper and not a response to chatter. Mechanics live in tools/lifecycle.py; the canonical doctrine is doctrine/session-routines.md.
disable-model-invocation: true
---

# Session-start (good-morning)

**Manual only.** Run this when an operator explicitly asks to "get oriented",
"good morning", or "catch up" -- never from ordinary conversation. The
canonical doctrine for *what* this routine is and *why* lives in
**`doctrine/session-routines.md`**; this skill only orchestrates it, so it never
restates that rationale here.

## 1. Run the mechanizable gather (read-only)

```
python tools/lifecycle.py session-start
```

It reports, without changing anything: commits since the last handoff (with a
graceful fallback on a fresh repo), working-tree state, open proposals/plans,
the active work-intents (if the coordination tool is installed), and the
resolved project interpreter.

## 2. Judgment steps (yours, not the tool's)

- Re-anchor on the governing doctrine and the deliberation record the gather
  surfaced -- read the load-bearing artifacts, not everything.
- Decide which in-flight thread, if any, you are picking up, and the state it
  resumes from.
- Confirm your role for the session before substantive work (see the roles
  doctrine) and name it explicitly.

Friendly alias: `/good-morning`.
