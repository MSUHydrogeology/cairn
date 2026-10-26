---
name: session-end
description: Manual lifecycle routine -- session-end (goodnight). Invoke only on an explicit operator request to wrap up; reflection-only by default. Not a conversational helper and not a response to chatter such as "goodnight". Mechanics live in tools/session.py; the canonical doctrine is doctrine/session-routines.md.
disable-model-invocation: true
---
<!-- cairn-internal-ref-allow: doctrine/session-routines.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: dev/reflections/next-session.md -->

# Session-end (goodnight)

**Manual only**, and **reflection-only by default.** Run this when an operator
explicitly asks to "wrap up" or "call it a night" -- never from ordinary
conversation ("goodnight, talk tomorrow" is not an instruction to scrub a
roadmap). The canonical doctrine for *what* this routine is and *why* lives in
**`doctrine/session-routines.md`**; this skill only orchestrates it.

## 1. Run the mechanizable step

```
python tools/session.py session-end $ARGUMENTS
```

`$ARGUMENTS` is whatever follows the command (e.g. `/session-end --handoff`):

* **(no arguments) -- reflection-only, the safe default every agent runs.**
  Scaffolds your per-session reflection file and surfaces open threads; writes
  nothing destructive.
* **`--handoff` -- the full handoff, the designated full-handoff owner only.**
  Preview first (changes nothing): `python tools/session.py session-end
  --handoff --dry-run`. Then run it with the owner marker:

  ```
  CAIRN_HANDOFF_OWNER=1 python tools/session.py session-end --handoff
  ```

  The marker is an **anti-accidental-run gate, not an authorization control**;
  a fail-closed lock prevents two concurrent owners from a double roadmap-scrub.
  The CLI runs only the mechanizable steps: prune reflections, metrics, surface
  active intents, and **prune the work-intent log** -- the one step that
  *rewrites* a coordination surface. It removes released claim/release pairs past
  a grace window (default 30d) and never removes an unreleased claim, which it
  reports instead. `dev/modules/coordination-tiers.md` specifies this as the
  goodnight *prune-intents* step; `--handoff --dry-run` lists it before it runs.

  **Run the full handoff last -- after other sessions have ended.** This is a
  precondition of the intent-log prune, not just tidiness. The prune *rewrites*
  the same file that ordinary `claim` / `release` **append** to, and those
  appends hold no lock; the fail-closed lock above serializes two *handoffs*,
  never a handoff against a live session. So a session appending during the
  rewrite can lose one advisory record. The prune refuses while any unreleased
  claim is newer than the claim-TTL, and skips if the file changes underneath
  it -- but running last is what makes the window *quiet* rather than merely
  narrow. Worst case if you ignore this: a warning row that never clears, on a
  gitignored local file, fixable by appending one release line.

## 2. Judgment steps (yours, not the tool's)

**Fill in the reflection** -- what shipped, what went well, what went wrong and
the lesson, what threads stay open -- and migrate any durable observation out to
doctrine or the roadmap before it is pruned. For a full handoff the **roadmap
scrub, the local next-session note, and the handoff commit** are also yours;
the note is never committed.

**The next-session note** is `dev/reflections/next-session.md`, a file the
reflections ignore line already covers. It is a convenience, not a record: the
board, the plans and the issues carry the handoff, and the first task is the
operator's call. Do not copy text from an issue, a web page or a comment into
the note; cite it by number or path. If the path is a link or a folder, or
`dev/reflections` or `dev` is a link, or
`git ls-files dev/reflections/next-session.md` prints it, do not read or write
the note; tell the operator. Before you write it, run
`git check-ignore -q dev/reflections/next-session.md`. If it exits 0, the path is
ignored. If it exits 1 and git does not track the path, add it to `.gitignore`
first. If it exits any other way, stop and tell the operator. Begin the note
with the date and the short commit id it was written at, and cite a commit, a
file or a board row for each claim.

**Run any project-specific close-out steps** recorded in
`dev/rules/custom_session_routines.md` (the `## Goodnight` section), if present
-- the adopter's concrete routine (doc builds, changelog cadence, test
invocations, foldback capture) lives there, not in this generic skill. A missing
file or a missing section means no custom steps.
