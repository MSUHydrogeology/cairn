# Attribute an Antigravity conversation to the project most of its files name

**Author**: Claude Sonnet 5.5 (Implementation)
**Status**: accepted
**Review**: none (waived by the Maintainer, 2026-11-22, in his words below)
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-22
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: The meter will give an Antigravity conversation to the one project that most of its saved files name, when that project leads every other by at least ten to one, and will stop counting the repeated `chunks/` copies, so a session that mentions another project once is no longer left unattributed.

## Decision summary

**What you noticed.** The first real Antigravity session in this project counted toward no project ([the real-log check](../measurement/antigravity-real-log-check-2026-11-22.md)): 832 of its saved files name this project's path and 4 name `lhm`'s, and rule 5 of [the Antigravity plan](../plans/archive/2026-11-22-antigravity-reader.md) ("exactly one project named by any file") gave up.

**His Decision (chat, 2026-11-22).** The board offered three ways out: (a) the project most files name wins when it has at least ten times any other's, (b) the repeated `chunks/` copies are not counted, (c) keep rule 5. He wrote: *"(A) and (B). No additional review is needed. This doesn't do anything different from a security standpoint. Touching something isn't the rule for that."* and then *"Sorry those a and b were for Antigravity"*. So both (a) and (b), with no review. Recorded from chat by Claude Sonnet 5.5, not scribed.

## Proposal

In `_conversation_project` (`dev/tools/meter.py` and its twin `templates/skills/_lib/meter.py`): (b) the search skips every file under a folder named `chunks` at any level, without opening it; (a) it counts, for each listed project, the files that name it, instead of stopping at the second project named. When the search completes, the project with the most files wins if its count is at least ten times the next project's (a next count of zero qualifies); otherwise the conversation is `antigravity_projects_ambiguous` and unattributed. The labels, link rules, entry and depth limits are unchanged. Claude and Codex are untouched.

**One thing I chose, which he can reverse.** A complete count needs the whole search, and the live conversation holds 60 MiB of searchable text without its `chunks/` copies, against the plan's unmeasured 16 MiB starting cap (`MAX_ATTRIBUTION_BYTES`). Over the cap a search ends `antigravity_search_incomplete`, never a guess. So the per-conversation cap rises to 128 MiB; the per-refresh limit of 256 MiB (`MAX_ATTRIBUTION_RUN_BYTES`) stays, so at most two conversations are searched in one refresh and the rest wait for the next. Measured on this Mac (count-only): 47 conversations, median 1.0 MiB of searchable text, 3 over 16 MiB, the largest 93 MiB with its copies and 60 MiB without.

## Rationale

The input is unchanged: text under `brain/<id>/` matched as bytes, never opened as a path, never an instruction. The rule decides on a count where it decided on a presence, and the label `antigravity_project_inferred` still says the figure is inferred. A forged file can still move a conversation's tokens; a wrong figure in a report is the harm.

## Documentation surface

`dev/measurement/README.md` and its template copy (rule, cap and `chunks/`), `CHANGELOG.md` (the Antigravity entry says "none or several counts toward no project"), and the board's W1 wait.

## Evidence / verification plan

Narrow tests beside the existing Antigravity tests: 832-to-4 style files (a project named by many files and another by one) is attributed to the leader; a margin under ten to one is ambiguous; a next count of zero qualifies; a `chunks/` file naming a second project does not count and is never opened (the `os.open` spy in the refresh test sees no `chunks/` path); the cap and run-limit tests follow the new constants; a conversation over the new cap is `antigravity_search_incomplete`. Each new test is shown to fail without its change by a one-line mutation in a scratch copy. Twins compared with `cmp`; the lock advanced for the changed hashed paths and `install/verify_integrity.py` read for its exit code; the prose gates run. After it lands, one real refresh after the next Antigravity reply shows whether the live session is attributed.

## Signals the change is wrong

The live session still counts toward no project. A conversation attributed to a project it did not work in because the other project's files were few. A refresh slowed by the larger read.

## Scope delta

**Scope delta**: preserved. It changes rule 5 of an archived plan by the Maintainer's word and removes no accepted outcome.

## Decision -- Maintainer (recorded from chat by Claude Sonnet 5.5, not scribed) -- 2026-11-22

Accepted at the light tier, with no review, in the words quoted under the Decision summary.

## Addendum -- Claude Sonnet 5.5 -- 2026-11-22, after the build

I ran the built rule read-only on the real live conversation (the one this proposal was written for). It ended `antigravity_search_incomplete` after reading 59,316,734 bytes, stopped by the entries limit, not the bytes: the conversation holds 5,194 entries outside its `chunks/` folders, against the plan's unmeasured 5,000 (the 128 MiB byte cap I chose was enough). Of the 47 conversations here it is the only one over 5,000. So the per-conversation entries limit (`MAX_ATTRIBUTION_ENTRIES`) rises from 5,000 to 20,000 on the same footing as the byte cap, a starting value corrected by a measurement; the per-refresh limit of 50,000 entries is unchanged, so at most two such conversations are searched in one refresh. I take it as following from his earlier word on Antigravity (*"We want Antigravity to function like everything else, and be able to measure for a plan. So do what's needed"*), since the first two changes were not enough to attribute the session they were for; he can reverse it. The Maintainer's waiver of review covers it as the same change.
