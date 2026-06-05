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

## 1. Run the mechanizable gather + skills self-heal

```
python tools/lifecycle.py session-start
```

It **reports** (read-only): commits since the last handoff (with a graceful
fallback on a fresh repo), working-tree state, open proposals/plans, the active
work-intents (if the coordination tool is installed), and the resolved project
interpreter.

It then performs **one idempotent write** -- the *skills fan-out self-heal*:
it ensures every eligible, in-use symlink-tier read-path (today only Claude
Code's `.claude/skills`) points at the canonical `.agents/skills/` source, so
an adopter established by lockfile-copy -- or whose harness was absent at
install -- gets working skills with no manual step. It is a no-op when already
linked, and never clobbers a divergent target (it refuses or quarantines). The
mechanics live in `tools/lifecycle.py`; this skill never reimplements them.

## 2. Judgment steps (yours, not the tool's)

- Re-anchor on the governing doctrine and the deliberation record the gather
  surfaced -- read the load-bearing artifacts, not everything.
- Identify candidate next steps, threads in flight, and their resumption state.
- Confirm your role for the session before substantive work (see the roles
  doctrine) and name it explicitly.
- Run any project-specific orientation steps recorded in
  `dev/rules/custom_session_routines.md` (the `## Session start` section), if
  present. A missing file or a missing section means no custom steps.
- **Do not act autonomously.** Session-start is orientation, not execution:
  present the orientation summary, name the candidate pickups and your role,
  then **stop** -- do not begin substantive work (implementing, editing doctrine
  or code, staging, or committing) until the operator has given a direction,
  which may already be in their opening message. (The tool's one self-heal write
  in step 1 is the only exception -- and it is the tool's, not yours.)
