---
name: session-end
description: Manual lifecycle routine -- session-end (goodnight). Invoke only on an explicit operator request to wrap up; reflection-only by default. Not a conversational helper and not a response to chatter such as "goodnight". Mechanics live in dev/tools/session.py; the canonical doctrine is Cairn's published session-routines method.
disable-model-invocation: true
---
External-repo paths: `docs/methodology/session-routines.md`

# Session-end (goodnight)

**Manual only**, and **reflection-only by default.** Run this when an operator
explicitly asks to "wrap up" or "call it a night" -- never from ordinary
conversation ("goodnight, talk tomorrow" is not an instruction to scrub a
roadmap). The canonical doctrine for *what* this routine is and *why* lives in
**Cairn's published session-routines method**; this skill only orchestrates it.

## 1. Run the mechanizable step

```
python dev/tools/session.py session-end $ARGUMENTS
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
  python dev/tools/session.py session-end --prepare-handoff
  ```

## 2. Judgment steps (yours, not the tool's)

**Fill in the reflection** -- what shipped, what went well, what went wrong and
the lesson, what threads stay open -- and migrate any durable observation out to
doctrine or the roadmap before it is pruned. For a full handoff the **roadmap
scrub, the local next-session note, and the handoff commit** are also yours;
the note is never committed.

The handoff commit message starts with the marker `Handoff`, in any letter
case; `session-start` lists the commits after the last one. A project with
another marker passes `--handoff-marker`.

Check that applicable roadmap and changelog entries were made at the commit or
archive that finished the work. Session end checks for omissions; it is not the
normal time to reconstruct entries that were due earlier.

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
-- the adopter's concrete routine (doc builds, changelog cadence,
foldback capture) lives there, not in this generic skill. A missing
file or a missing section means no custom steps.

At every explicitly requested goodnight, including reflection-only, run
`python dev/tools/meter.py refresh --report --json` once when Meter is installed.
If a project-specific Goodnight step runs that same report, use its result and
do not refresh a second time for this report. Put the complete sanitized
`cairn-pulse/1` record in the reflection on success. If the output is a closed
Meter receipt such as `partial`, `unavailable` or `disabled`, report its status
and reason exactly; never turn missing or failed usage into zero, include raw
child diagnostics, or read an older project aggregate. If it exits without a
valid pulse or closed receipt, report unavailable without the raw diagnostic.
Do not commit the per-project aggregate. The full-handoff lock's separate
pre-prune refresh still runs and retains its existing fail-closed behavior.

Reflection-only participants acquire no test obligation. Slow tests remain due at release and
whenever an accepted plan, safety or security requirement, or the Maintainer
requires them. Change checks and Boundary B remain due on their existing
schedule.

## 3. Give the user the guarded prune command

After the reflection, roadmap scrub, next-session note, custom steps and
handoff commit are complete, check for unreleased claims newer than the claim
TTL and confirm that no session is appending to the intent log. A ledger scan
cannot establish that there is no live appender or guarantee future quiet. If
either condition is uncertain, state the unresolved condition beside the
command. Do not run the prune as the agent.

Give the user this exact command, in the form for the shell the session uses
(give both if you do not know). In bash or zsh:

```
CAIRN_HANDOFF_OWNER=1 python dev/tools/session.py session-end --handoff
```

In PowerShell, which cannot set a variable in front of a command, set it for
this one run:

```
$env:CAIRN_HANDOFF_OWNER = '1'; python dev/tools/session.py session-end --handoff; Remove-Item Env:CAIRN_HANDOFF_OWNER
```

The command may repeat the reflection preview. Under the existing
designation-marker and fail-closed lock guards, it prunes eligible reflections,
surfaces active intents, and attempts to prune eligible released intent pairs.
The marker is an anti-accidental-run gate, not an authorization control. The
command does not fill in the owner's reflection or perform the scrub, note,
custom steps or handoff commit.
