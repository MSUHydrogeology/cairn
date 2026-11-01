---
name: session-end
description: Manual lifecycle routine -- session-end (goodnight). Invoke only on an explicit operator request to wrap up; reflection-only by default. Not a conversational helper and not a response to chatter such as "goodnight". Mechanics live in tools/session.py; the canonical doctrine is docs/methodology/session-routines.md.
disable-model-invocation: true
---
<!-- cairn-internal-ref-allow: docs/methodology/session-routines.md reason=docs/methodology/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where docs/methodology/ references resolve") -->

# Session-end (goodnight)

**Manual only**, and **reflection-only by default.** Run this when an operator
explicitly asks to "wrap up" or "call it a night" -- never from ordinary
conversation ("goodnight, talk tomorrow" is not an instruction to scrub a
roadmap). The canonical doctrine for *what* this routine is and *why* lives in
**`docs/methodology/session-routines.md`**; this skill only orchestrates it.

## 1. Run the mechanizable step

```
python tools/session.py session-end $ARGUMENTS
```

`$ARGUMENTS` is whatever follows the command (e.g. `/session-end
--prepare-handoff`):

* **(no arguments) -- reflection-only, the safe default every agent runs.**
  Scaffolds your per-session reflection file and surfaces open threads; writes
  nothing destructive.
* **`--prepare-handoff` -- the designated full-handoff owner only.** This
  scaffolds the reflection, surveys open threads, surfaces active intents when
  `intent.py` is installed, and emits the prune preview, capture prompt and
  rate-limit output. It does not invoke either prune helper or change existing
  reflection files or the intent log. The intent listing is only a snapshot: it
  cannot prove that no session is appending now or that the log will stay quiet.
  `--dry-run` also suppresses the reflection scaffold.

  ```
  python tools/session.py session-end --prepare-handoff
  ```

## 2. Judgment steps (yours, not the tool's)

**Fill in the reflection** -- what shipped, what went well, what went wrong and
the lesson, what threads stay open -- and migrate any durable observation out to
doctrine or the roadmap before it is pruned. For a full handoff the **roadmap
scrub, the local next-session note, and the handoff commit** are also yours;
the note is never committed.

**The next-session note** is `next-session.md` in `dev/reflections/`, a file the
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

## 3. Give the user the guarded prune command

After the reflection, roadmap scrub, next-session note, custom steps and
handoff commit are complete, check for unreleased claims newer than the claim
TTL and confirm that no session is appending to the intent log. A ledger scan
cannot establish that there is no live appender or guarantee future quiet. If
either condition is uncertain, state the unresolved condition beside the
command. Do not run the prune as the agent.

Give the user this exact command:

```
CAIRN_HANDOFF_OWNER=1 python tools/session.py session-end --handoff
```

The command may repeat the reflection preview. Under the existing
designation-marker and fail-closed lock guards, it prunes eligible reflections,
surfaces active intents, and attempts to prune eligible released intent pairs.
The marker is an anti-accidental-run gate, not an authorization control. The
command does not fill in the owner's reflection or perform the scrub, note,
custom steps or handoff commit.
