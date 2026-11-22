# Name the project at session start, and keep each agent's log folder current

**Author**: Claude Sonnet 5.5 (Implementation), from the Maintainer's idea
**Status**: accepted
**Review**: none (waived by the Maintainer, 2026-11-22, in his words below)
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-22
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Session start prints one fixed line naming the project, so the usage meter can tell which project an Antigravity conversation belongs to without guessing from file text. A second part, a check that each agent's log folder is still where the meter looks, is held.

## Decision summary

**What you noticed.** The first real Antigravity session in this project counted toward no project ([the check](../measurement/antigravity-real-log-check-2026-11-22.md)): 832 of its files name this project's path and 4 name `lhm`'s, and the rule "exactly one project named by any file" gave up. The Maintainer's idea (chat, 2026-11-22): *"We could have a session start routine that updates the log locations for each agent. That way we can capture activity properly."*

**The change.** (A) `session.py session-start` prints one line, `cairn-meter-project: <the project's root path>`, which lands in the agent's saved conversation. The meter looks for that line first. (B) A read-only command, `meter.py roots`, reports whether each listed log folder exists and whether a known agent's default folder exists but is not listed; session start tells the person and offers a fix, and never edits the consent file without a clear yes.

**His Decision (chat, 2026-11-22), on being told both need a Security Review pass and that the session-start skill is touched:** *"(A) and (B). No additional review is needed. This doesn't do anything different from a security standpoint. Touching something isn't the rule for that."* This is recorded from chat by Claude Sonnet 5.5, not scribed. The review is waived on his word; my reading of why it holds is under Rationale.

## Proposal

**A. The marker.** Session start prints, as its first line, `cairn-meter-project: ` and the project root exactly as `git rev-parse --show-toplevel` gives it. In `_conversation_project` (`dev/tools/meter.py`, and its twin `templates/skills/_lib/meter.py`) each searched file is also matched for that prefix followed by a listed project's path, under the same byte-before and byte-after rules as a path today. The projects named by a marker decide: exactly one is the project; two or more are ambiguous (`antigravity_projects_ambiguous`, unattributed); none falls back to today's path rule unchanged. The limits, the link rules and the labels are unchanged, and a marker-attributed conversation still carries `antigravity_project_inferred`. Claude and Codex are untouched.

**B. The roots check (held: not built; see the last Decision).** `python tools/meter.py roots` prints, for each source in the consent file, its alias, its tool and `present` or `missing`; and, for each of Claude (`~/.claude/projects`), Codex (`~/.codex/sessions`) and Antigravity (`~/.gemini/antigravity`) whose default folder exists but is not listed, `not listed`. It lists names and states only: no path, no file text, no log read, one `stat` per folder. The session-start skill (both copies) runs it only at an attended start when an enabled consent file exists, says what it found, and offers to change the file only with a clear yes, as its meter-setup offer already does.

## Rationale

Part A only; B adds no input. The marker is the same kind of input the meter already trusts: text under `brain/<id>/` matched as bytes, never opened as a path, never an instruction. It is narrower than a bare path, since it needs the prefix and the path together, and it is declared by the agent where today's path is incidental. It grants nothing and no gate reads it; its weakness is the existing one, a forged line moves a conversation's tokens and the harm is a wrong figure in a report, marked inferred. The roots check reads no log and writes no file, so it adds no new input.

## Documentation surface

`dev/measurement/README.md` and its template copy (the marker and `roots`), both `session-start` skill files, `CHANGELOG.md`, and the plan's board wait (W1) in `dev/PLANNING.md`.

## Evidence / verification plan

Narrow tests only. (A) A conversation whose files name two projects by path and one by marker is attributed to the marker's project; two different markers are ambiguous; no marker falls back to the path rule; a marker for an unlisted path counts as none; a marker split across a 64 KiB block edge is found; and `session.py session-start` prints the line first with the root, on a clean and a dirty tree. (B) `roots` on a temporary home: a listed present folder, a listed missing one and an unlisted default, with no path in its output and no file written. Each new test is checked to fail without its change, by a one-line mutation in a scratch copy. The twins are compared with `cmp`; the lock is advanced for the changed hashed paths and `install/verify_integrity.py` is read for its exit code; the claim, link and snippet gates and `tests/check_cairn.py` are run on the prose. No whole-suite run.

## Signals the change is wrong

A real session in this project that still counts toward no project after a session start. A conversation counted toward a project it did not work in because a marker was copied into it. A refresh that fails or slows because of the marker search.

## Scope delta

**Scope delta**: preserved. It adds to the accepted usage-counting work and removes nothing accepted.

## Decision -- Maintainer (recorded from chat by Claude Sonnet 5.5, not scribed) -- 2026-11-22

Accepted at the light tier, with no review, in the words quoted under the Decision summary.

## Decision -- Maintainer (recorded from chat by Claude Sonnet 5.5, not scribed) -- 2026-11-22, later

Told that part B was being built with part A, he wrote (chat, 2026-11-22): *"Let's hold off on 2"*. Part B (the `meter.py roots` check and the session-start offer) is therefore **not built**. It stays in this proposal as written, and is taken up only on his word. Part A proceeds as accepted.
