# Plan: Count Claude usage toward a project

**Source proposal**: dev/proposals/archive/2026-11-21-claude-usage-counting.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/custom_session_routines.md, dev/rules/protected-surfaces.md, dev/rules/development-environment.md
**In brief**: The usage meter counts Claude's own token use toward a project, by the working folder each Claude record names, so the end-of-session report stops showing Claude usage as unknown.

## Build summary

After this plan the meter counts a Claude record toward a project when the record's own working folder is the project's or inside it, its log sits under a folder the Maintainer approved, and the project's Git remote checks out. Sub-agent transcripts count the same way. Summaries of finished sub-agents are not counted; a reading whose summaries cannot be tied to a transcript prints INCOMPLETE. The meter's private ledger gets a new version, so the first refresh refuses the old one until it is moved aside. The new ledger starts at zero and counts only what is written after its first refresh, for every tool. One rule sentence and a list of field names that may be shown go beside the consent rule. Only the existing meter and its tests change, in five chunks.

## Source proposal

The Maintainer accepted the proposal at the heavy tier on 2026-11-21 with all five of Strategy's picks: the Antigravity look happens later on his Mac; a record from a work folder inside the project counts; no table for each agent run; built for v0.8.1 (the Maintainer's Decision of 2026-11-21 moved it from v0.9); the meter's ledger is rebuilt from the logs still on disk. The plan executes it and reopens nothing. Antigravity is not in this plan. Exact names, conditions and test inputs are in the companion `dev/plans/2026-11-21-claude-usage-counting-detail.md` ("Detail", D0 to D7), part of this plan; it exists so the opening text stays short and a low-tier agent invents no design.

## Scope

**Result.** The Pulse shows Claude usage for the project by kind of token (fresh input, cache writes, cache reads, output), with cost data that no longer depends on a hand-kept record that measured the wrong thing.

Proposed paths:
- `tests/test_meter_claude_usage.py`

**Measured by Strategy on 2026-11-21, counts only, one project's logs** (90 log files, 9,609 assistant records with usage): 4,333 distinct messages, none under more than one session id. No record of the four skipped types held a `usage` key. The folder equalled the configured project path exactly in 3,539 records and lay exactly inside it in 59; none differed only by letter case or separators, none lay outside. There were 84 summaries and 89 sub-agent transcripts; no summary's own id equalled a transcript's agent id, but the text of every one of the 84 names exactly one transcript's agent id. Every summary also holds its own run's id inside a fixed frame the tool writes, `<task-id>`, the id, `</task-id>` (87 of 87; Detail D7, P4). The incomplete rule rests on that frame, not on every run of letters in the text: a summary is covered when its frame names exactly one id and a transcript of that run, in the same session, was read; a summary with no frame, or two different ids in frames, or a run not read, makes the reading incomplete. This leans on the tool's wording; a tool version that changes it turns readings incomplete, never whole.

**Why code, not written steps** (the Maintainer, 2026-11-21: "no new tooling unless it's needed"). Nothing new is a script or an option. Each piece added to the meter, with its reason:
- The folder rule (`_project_for_folder`): the text of every record's folder must be compared the same exact way thousands of times, and an agent following steps would miss a case.
- The Claude branch's proof of ownership: whether a record counts is decided by the code that counts, so the same record gets the same answer.
- The summary test (`_usage_values`, `_summary_run`): a record is a summary only on an exact shape, and any other record carrying `usage` must never pass as harmless.
- The ledger's memory (`agent_runs`): logs are read in pieces over many refreshes, so no one pass sees a summary and its transcript, and the count that links them must survive between runs.
- The version change: the meter already refuses an old ledger by this rule.

The rule sentence, the field-name list, the README and the changelog are written steps, not code.

**Limits stated.** (1) A folder link inside the project counts as inside, since the folder is compared as text. (2) A message seen under two folders or two sessions becomes unknown in one reading, and across refreshes when both folders map to a project; a repeat across refreshes where one folder lies outside every project is not caught. (3) Past 1,000 uncovered summaries or 100,000 transcripts, the meter cuts the excess and prints INCOMPLETE; it never fails a refresh over it. (4) The summary's three field names and the keys `isSidechain` and `agentId` were confirmed by Strategy on 2026-11-21 (Detail D7, P1 to P3). The author's first guess at the three names was wrong, and Detail D0 now holds the confirmed ones; they hold for the tool version measured. (5) The incomplete rule sees only summaries, and on the measured logs all 85 were in the main log: none was in a transcript, and ten of the 90 transcripts were named by no summary. By Strategy's reading those ten include runs that another agent started. Such a run is counted from its transcript like any other, but if its transcript were missing, nothing would mark the reading incomplete. (6) The frame is the tool's wording, so a tool version that drops or changes it turns readings incomplete, never whole. One residual: if a version dropped its own frame and a model's text carried a frame naming a run whose transcript was read, that summary would be called covered. And a model's text that quotes another run's frame makes its summary untied, so the reading says INCOMPLETE until the ledger is replaced. (7) A sub-agent that finished between its last record and a new ledger's first refresh leaves its summary untied for good: the reading says INCOMPLETE until the ledger is replaced.

**Reuse.** The Codex project check (`_verified_project_remote`, the `verify_project` closure) and `_event_record` are reused as they are; the merge at the end of `read_records` already turns two bindings of one message into `conflicting_binding`. `_record_carries_usage` is replaced by `_usage_values`, the same walk, rather than a second walker. The Codex folder test is repeated in four lines, not shared, because the Codex tests pin `_codex_context`. Searched `dev/tools/` and `templates/skills/_lib/` for `cwd`, `isSidechain` and `usage`: only `meter.py` holds them.

**Doctrine surface.** `dev/rules/custom_session_routines.md` (one sentence and one list), `dev/measurement/README.md`, `CHANGELOG.md`. `dev/PLANNING.md` only has its two links to the proposal repointed.

**Stale records, and who refreshes each.** (a) `tests/fixtures/gate_manifest.json` holds a hash for `tests/integration/test_meter.py`, which this plan edits: it adds one line to the Maintainer's one signing, and no agent edits it. The other test files touched are not in that manifest (searched by name, 2026-11-21). (b) Cairn's own lock records the hash of `dev/tools/meter.py`: C5 refreshes it with the installer's scoped finalize over that file alone, in a commit that holds nothing else, then `install/verify_integrity.py --target .` must report OK. (c) The two meter copies must stay byte-identical: each code chunk copies and runs `cmp`; `tests/test_skills_install.py` and `tests/test_skills_upgrade.py` also check the copy. (d) No installer symbol changes, so no AST listing is owed.

## Sequence

C1 to C3 each end in the copy and `cmp`, one commit for each chunk, explicit paths only. The execution agents are Haiku; the plan's agent checks each diff against the criterion. The `/6` version change stays in C3 (the usual review's N4 asked for C1): the chunks merge together, no meter outside the build's work folder runs between them, and the branch's meter is not used for a real refresh before C3. The chunks are built in a separate work folder and merged into `0.9-dev` together, so no guarded handoff runs a C1 or C2 meter.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Folder proof, request key | plan review | `_project_for_folder`, the changed Claude branch, new test file and its tier entry |
| C2 | Summaries and transcripts | C1; Strategy's P1 to P4 | `_usage_values`, `_summary_run`, the batch's `agent_runs`, new reason |
| C3 | Ledger memory, versions | C2 | `agent_runs` in the ledger, coverage reason, `/6` versions, end-to-end tests |
| C4 | Rule and docs | C3 | rule sentence and list, README, changelog |
| C5 | Lock and joined run | C4 | refreshed lock, selection run and record |

## Acceptance criteria

**C1.** A Claude record whose `cwd` equals the project path or lies inside it, with a request id and a passing remote check, reads as `proven` and `current_local_verified`, with the project's alias. Each failing case in Detail D5 (outside, sibling name, trailing separator, other letter case, `..`, inside two projects, the Windows forms, failed remote check, unapproved root, no request id) stays unknown with its reason and has a passing control. One message under two sessions or two folders is one unknown event with `conflicting_binding`; equal repeats merge; differing usage gives `conflicting_usage`. A proven Claude event with a known time joins the per-artifact split only when exactly one closed, reliable claim for its project, tool and session covers its time; `_build_mappings` is not changed. Public entry: `meter.read_records`.

**C2.** A record with exactly the three summary fields and one id in frames is no event and leaves one summary row. Any other non-assistant, non-skipped record carrying `usage` adds `agent_runs_incomplete`, never `unsupported_record`; the four skipped types stay skipped whatever they hold. A sub-agent transcript record leaves one pair of keys. Each shape failure in Detail D5 has its control.

**C3.** After a refresh that reads a summary with no transcript, the export lists `agent_runs_incomplete` and the pulse prints INCOMPLETE; after one that reads the transcript, it does not. Another session's transcript, two different ids in frames, no frame, or a run not read leave it on; a record that could not be classified keeps it until the ledger is replaced. The ledger round-trips, each hand edit in Detail D5 is refused as `ledger_invalid`, and a `/5` ledger is refused with `ledger_old_schema` and left unchanged. Entries: `_refresh_ledger`, `_new_ledger`, `_load_ledger`, `pulse._parse_meter_aggregate`. End-to-end tests run on POSIX only (the Linux subsystem here).

**C4.** The rule sentence (Detail D6) is in `dev/rules/custom_session_routines.md` beside the consent rule, with the list of field names; the README and the changelog say what Detail D6 says. `python dev/tools/claim_check.py`, `link_check.py` and `tests/check_cairn.py` pass on each file.

**C5.** The lock is refreshed alone; `verify_integrity` reports OK; `cmp` of the two meter copies prints nothing; the nine selected files give no failure that is not the host's (compared before and after, Verification).

**Strategy's checks, not the build agent's** (they read private logs; the build agent must not attempt them). Before C2: P1 to P4 (Detail D7), which Strategy ran on 2026-11-21. After C3 and before code review: the proposal's developmental check, that the meter's Claude totals for one session, by kind of token, equal an independent count-only sum of its log and transcripts; it needs the old ledger moved aside first (choice 5), a first refresh to set the start, and a session written after it.

**Security (re-answered).** S1: input is log lines under approved roots; folders and ids are text, never opened; project paths and remotes come from the consent file. S2: each case in C1 to C3, with controls, leaves usage unknown or the reading incomplete. S3: the user's own `refresh`, over approved roots and configured projects. S4: it breaks toward unknown or INCOMPLETE, never a guessed number. S5: made-up usage written by anything that can write files as the user, the measured agents included, as for Codex (a wrong number in the report and export); a tool version that changes the summary shape makes readings incomplete; usage under another field name stays unseen.

## Scope delta

**Scope delta**: degraded -- (1) Antigravity counting, **disposition**: defer. Home: the Maintainer's Decision of 2026-11-21 on the proposal, "Yes. Claude and Antigravity are part of v0.8.1. Excluding them was a defect. I use all three every day. The same way that excluding Windows and Linux certification was a defect." So Antigravity gets its own plan, written after the count-only look on his Mac, and built before v0.8.1 is cut. It is not in this plan. (2) The ledger is not rebuilt from logs on disk: a new ledger counts nothing before its first refresh, for every tool, and the old ledger's events are lost. (3) A message repeated across refreshes in one session, with a folder outside every project, stays counted once under its first project. (4) A missing transcript that no summary names leaves the reading whole. **disposition** of (2) to (4): accept. Asked to allow them, or to have a back-fill designed for (2), the Maintainer wrote (chat, 2026-11-21): "Allow all three". His Decision is on the proposal.

## Verification

Changed promises: which Claude records count toward a project; summaries are not usage; a reading with untied summaries is INCOMPLETE; the ledger version. Entry points: `meter.read_records`, `_refresh_ledger`, `_load_ledger`, the pulse's reading of the export.

Test selection: `python tests/tier_inventory.py for dev/tools/meter.py templates/skills/_lib/meter.py` gave nine files on 2026-11-21. Chunks C1 to C3 run four of them plus the new file, which guard the changed promises: `tests/integration/test_meter.py`, `tests/test_meter_usage_free_records.py`, `tests/test_skills_install.py`, `tests/test_skills_upgrade.py` and the new `tests/test_meter_claude_usage.py` (listed in `tests/test_tiers.json` in C1, then `python tests/tier_inventory.py check`). C5 runs all nine once; the five not run earlier are `tests/security/test_git_read_routes.py`, `tests/test_security_lint.py`, `tests/test_session_failsafe.py`, `tests/test_session_routines.py` and `tests/test_session_writes_contained.py`. The Windows Server host fails many tests before any change, so each group runs once at the starting commit and once after, failing ids and messages are compared, and an id failing only after is rerun alone at both. POSIX-only tests run in the Linux subsystem, one run at a time.

Not run by the build agent: the real-log checks above. The broad selection, the Python 3.13 run and the joined run belong to the arc (`dev/PLANNING.md`, "What the joined run owes"). Prose gates (`claim_check`, `link_check`, `check_cairn`, `git diff --check`) run on every document changed.

## Plan review -- Claude Sonnet 5.5 (`claude-sonnet-5-5`) -- 2026-11-21

```
Reviewed commit: c385206a
```

**Obligation**: the usual plan review of "Plan review: required(Internal + Internal Security Review)"; the Security Review pass is still due.
**Tier**: Internal
**Findings**: raised (2 blocking, 5 non-blocking)
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes, and the build matches outcomes A to E except two gaps below -- `dev/tools/meter.py` 6623-6676 (today's Claude branch), D1 to D4.
2. **Best alternative.** No smaller design keeps the summary promise; no script or option is added; the three caps follow the ledger's other lists -- `dev/tools/meter.py` 3022-3110.
3. **What would show it wrong.** A sub-agent that finished just after the first refresh, so its transcript was only bookmarked and never read, leaves a summary uncovered for good -- `dev/tools/meter.py` 4260-4273.

The plan counts a Claude record by its own folder, ties summaries to transcripts by id, and fails toward unknown or INCOMPLETE. I walked a summary naming its transcript, none, two, one in another session, other-shaped `usage`, two summaries for one transcript, and a transcript with none: each is covered or INCOMPLETE. The folder rule matches D5 for every form the brief lists except three inputs (N1).

**Blocking**
1. **Choice 5 is not delivered (reduction; the Maintainer's call).** He accepted "rebuild the meter's ledger from the logs still on disk". A new ledger has no `starts`, so every log on disk is only bookmarked (`meter.py` 4260-4273; README: "counts nothing before that, and `rebuild` does not back-fill history"). Nothing comes back from logs on disk, for Codex as well; the old ledger's Codex events and daily totals are lost. D4's last bullet and D7 say so, the opening text does not. No exact words: allow it as a Scope delta (block A) or have Strategy design a back-fill.
2. **Limits (2) and (5) are reductions, so they belong under Scope delta.** The proposal says two folders make a message unknown, and lists "a reading called whole when transcripts were missing" as a sign of failure. (2) and (5) allow both. Only the Maintainer can allow that (block A).

**Non-blocking**
- N1. D5 lacks a missing, empty and 4,097-character `cwd`; add them to the `outside_stays_unknown` row.
- N2. INCOMPLETE can stay on for ever (an unclassified record; a transcript bookmarked or deleted). Clearing it means replacing the ledger, which costs history (blocking 1). Say so in the README sentence (D6).
- N3. D4 never gives the sort keys: use `(session_key, agent_key)` and `(session_key, names)`; `_validate_agent_runs` should also require `names` sorted and unique.
- N4. C1 changes the event key under an unchanged reader version; move the `/6` bump to C1, since the Maintainer's own session-end refresh runs this meter.
- N5. Claude events now reach `_build_mappings` (the claim-to-artifact split), which the plan does not mention or test.

Not covered: no test run, no log read, no Windows run of D1; the free-text summary rule and the consent file are the Security Review's. Over the 300-word target: two reductions need their evidence.

### Exact words (block A)

Replace the Scope delta section with: "**Scope delta**: degraded -- (1) Antigravity counting, **disposition**: defer, as written. (2) The ledger is not rebuilt from logs on disk: a new ledger counts nothing before its first refresh, for every tool, and the old ledger's events are lost. (3) A message repeated across refreshes in one session, with a folder outside every project, stays counted once under its first project. (4) A missing transcript that no summary names leaves the reading whole. **disposition** of (2) to (4): ask the Maintainer; set `**Waiting on Maintainer**`." Then delete "so reviewers decide whether it is a reduction" from Limits (2).

## Plan review -- Claude Opus 5.5 (`claude-opus-5-5`) -- 2026-11-21

```
Reviewed commit: e73fc37653537660a0e13606f4e01ff1640f4081
```

**Obligation**: the Internal Security Review of "Plan review: required(Internal + Internal Security Review)".
**Tier**: Internal Security Review
**Findings**: raised (1 blocking, 4 non-blocking)
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes: log text never chooses what is opened (only a configured project's `.git/config`, read directly, no Git run), and folders and ids reach the ledger only as digests -- `dev/tools/meter.py` 5925-5958, 6096.
2. **Best alternative.** Comparing the folder as text is the safer choice: opening it would let log text send the meter to any path, a network share included; text lets through only links inside the project (Limit 1) -- `meter.py` 1644-1655.
3. **What would show it wrong.** A test where a summary names its own run, whose transcript was never read, and one sibling run whose transcript was read: D4 as written calls it covered -- Detail D4, second bullet.

The design fails toward unknown on every path that web or repository text can reach; forged logs stay S5, as for Codex. Old copied messages are dropped by the start and fold rule (`meter.py` 4050-4057), so a fold cannot count twice.

**Agreement.** The usual review's blocking 1 and 2 and N2 to N4 hold. If the Maintainer picks a back-fill for choice 5, it reads logs written before the start rule and needs its own security look.

**Blocking**
1. **A missing transcript can be called covered.** A summary names its own run; if that transcript was never read (bookmarked at the first refresh, or deleted) and the model-written text also quotes one sibling run, the one match is the sibling and the reading prints whole. Agents quote each other's ids. Maintainer's call: block S, item 1.

**Non-blocking**
- S1. `_summary_names` collects every run before the cap: one 8 MiB line gave 888,888 runs (pattern linear: 0.4 s, typed strings). Stop at the cap (block S).
- S2. Merging all of `agent_runs` after every batch repeats the full sort per file. Gather per batch; merge once (block S).
- S3. `agent_runs` spans every session under every approved root and never ages; two quoted ids or 257 hashes leave every project INCOMPLETE until the ledger is replaced (block S, with N2).
- S4. Reading question: the D6 rule weakens nothing, but forbids the record type names the plan's tests use (block S).

Not covered: no log, consent file or ledger read; the Windows refresh route and the pulse's printing not traced. Plan S1, S3 and S4 hold; S2 and S5 need blocking 1. Over target: the blocking case needs its path.

### Exact words (block S)

1. In block A, after item (4) add: "(5) A summary whose own transcript was never read counts as covered when its text also names one other run of its session whose transcript was read." and make its disposition cover "(2) to (5)".
2. Detail D3.2: replace "collect `_digest("agent-id", run)` of each into a set. Return `[]` when the set holds more than `MAX_SUMMARY_NAMES`, else the sorted list." with "add `_digest("agent-id", run)` of each to a set, and return `[]` at once when the set would hold more than `MAX_SUMMARY_NAMES`; otherwise return the sorted list."
3. Detail D4: replace "`merged = _merge_agent_runs(agent_runs, batch["agent_runs"])`, then `agent_runs.clear()` and `agent_runs.update(merged)`." with "add the batch's transcript and summary rows, as tuples, to two sets kept under `agent_runs`, and its `unclassified` to the count (at most `MAX_COUNTER`); nothing is covered, cut or sorted there. `_new_ledger` turns the sets into D3.5's sorted lists before its one `_merge_agent_runs` call."
4. Detail D6, README bullet: after "prints INCOMPLETE" add "; the runs are kept for every session under the approved roots, so one untied summary anywhere marks every project, and it clears only when the ledger is replaced".
5. Detail D6: replace "and the three in `_SUMMARY_FIELDS`. The list is the keys the reader reads, nothing more." with "the three in `_SUMMARY_FIELDS`, and the record type names `assistant`, `attachment`, `user`, `system`, `progress` and `file-history-snapshot`. The list is the keys the reader reads and the type names the plan's tests use, nothing more."

## Plan response -- Claude Sonnet 5.5 (`claude-sonnet-5-5`; Implementation, for the author) -- 2026-11-21

Both reviews are folded into the plan and its Detail. Status stays `revising-plan`: Scope delta items (2) to (4) wait on the Maintainer (`**Waiting on Maintainer**` set), and the changed summary rule needs one limited Security Review before the plan can be built.

Usual review:
1. Blocking 1 and 2: taken; block A replaces the Scope delta, with item (1) homed in the Maintainer's Decision of 2026-11-21 and items (2) to (4) left to him. Limits (2) lost its "reviewers decide" clause; Source proposal now says v0.8.1; Build summary says the new ledger starts at zero for every tool.
2. N1: taken (three `cwd` inputs in D5).
3. N2: taken (README sentence in D6, Limit 7).
4. N3: closed by Security decision below (one sort key; validation requires sorted and unique).
5. N4: not taken; the `/6` change stays in C3, reason in Sequence.
6. N5: taken; one sentence in C1, one row in D5; `_build_mappings` needs no change.

Security Review:
1. Blocking 1: closed by tying a summary to its run through the tool's fixed frame `<task-id>` (D0, D3.2, D3.3, D5); block A's item (5) is not added. This is a substantive change to the reviewed summary rule, so this step gets one limited Security Review.
2. S1: closed by the same change (the walk stops at the second distinct id; no name cap remains).
3. S2: taken, reworded for pair rows (D4: sets per batch, one merge per refresh).
4. S3: taken (README sentence; Limit 7).
5. S4: taken, with `task-id` added (D6).

Not run: any test, log read or meter run.

**Elapsed**: unknown. **Tokens**: unknown.

## The Maintainer's allowance -- recorded by Claude Fable 5.2 (Strategy) -- 2026-11-21

Strategy put the Scope delta's items (2) to (4) to the Maintainer in these words: "1. The restart. When this lands, the meter's running record starts again at zero for all three tools, and nothing already in the logs is counted. The old record file is kept aside. 2. A rare folder case. If one message's records fall into two meter readings, and the working folder moved outside the project in between, the message stays counted for the project. I did not see it in 4,333 measured messages. 3. Sub-agents started by sub-agents. They leave no summary record. If such a transcript file went missing, the reading would not say INCOMPLETE. When the file is there, its usage counts normally." The choices were "(a) Allow all three", which Strategy recommended, and "(b) Allow 2 and 3, and I design a back-fill for the restart". He wrote (chat, 2026-11-21):

> "Allow all three"

What that settles:

- **Items (2), (3) and (4) are accepted** as written in the Scope delta. No back-fill is designed. The scribed Decision is the last section of the source proposal.
- **The Waiting line is removed.**
- **Still due before the plan can be built:** one limited Security Review of the changed summary rule, as the response says. Status stays `revising-plan` until it is in.

**Elapsed**: unknown. **Tokens**: unknown.

## Plan amendment review -- Claude Opus 5.5 (`claude-opus-5-5`; Security Review) -- 2026-11-21

**Prior reviewed commit**: e73fc37653537660a0e13606f4e01ff1640f4081
**Replacement commit**: 647ab29313c35d8c9149a0a171044d0704cc398a
**Affected cells and dependencies**: Scope, Sequence, Acceptance criteria, C2, C3, C4
**Obligation**: Internal Security Review
**Verdict**: ACCEPT

**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**:

1. The frame closes blocking 1: text outside a frame is never read, so the sibling's id no longer counts, and the pair with the unread run stays uncovered -- Detail D3.2, D4 (set difference).
2. Every forged frame beside the tool's own one gives `""`, never covered; the work per record is linear, bounded by the 8 MiB line -- `meter.py` 49, 6613; typed-string timing below.
3. What would show it wrong: a tool version without its own frame, with a model's frame naming a read run (Limit 6, stated) -- Detail D7, P4.

**Checked.** Walked the old case by hand: INCOMPLETE. Forged frames: sibling beside the tool's frame gives `""`; same run gives one id; a frame split over two strings, in a key, with a 7- or 65-character id, or an upper-case tag is not matched; two cases of one id are two ids, `""`. Timing (`python -I -c`, typed 8 MiB strings, `finditer`): at most 0.14 s. `None` and `""` take one path (D3.3). Ledger rows: hand edits can delete rows, as before (S5). First review: blocking 1 and S1 to S4 are closed by what the response names.

**Non-blocking**
- N1. A model's result quoting another run's frame makes the summary `""`, INCOMPLETE until the ledger is replaced; state it (block R, 1).
- N2. Say the pattern runs on each string separately; test the unmatched forms (block R, 2 and 3).
- N3. Row key set not pinned in validation (block R, 4).
- N4. The `/6` reason holds only if no chunk lands alone on a branch whose guarded handoff runs `meter.py refresh` (`dev/tools/session.py` 1954-1965) (block R, 5).
- N5. C2 still says "exactly the three summary fields" with no frame; D6's list now holds names that are not field names (block R, 6 and 7).

Not covered: no log, ledger or consent file; no test run; unparsable summary lines (`invalid_record`, one refresh only) are older behaviour; out-of-scope cells.

### Exact words (block R)

1. Limits (6): after "that summary would be called covered." add "And a model's text that quotes another run's frame makes its summary untied, so the reading says INCOMPLETE until the ledger is replaced."
2. Detail D3.2: replace "collect the distinct ids that `_SUMMARY_FRAME` finds" with "collect the distinct ids that `_SUMMARY_FRAME.finditer` finds in each string value on its own".
3. Detail D5, `summary_run` row: add inputs "a frame only inside a key; a frame split across two strings; `<TASK-ID>`; a 7-character id" with expected "`""`" each.
4. Detail D4, `_validate_agent_runs`: after "the three keys exactly;" add "every row a dict with exactly the keys `session_key` and `agent_key`;".
5. Sequence: after "before C3." add "The chunks are built in a separate work folder and merged into `0.9-dev` together, so no guarded handoff runs a C1 or C2 meter."
6. C2: replace "A record with exactly the three summary fields is no event and leaves one summary row." with "A record with exactly the three summary fields and one id in frames is no event and leaves one summary row."
7. Detail D6: replace "and field names on the list kept in this file; any other field name" with "and names on the list kept in this file; any other name", and "Field names that may be shown" with "Names that may be shown".

## Plan response to the amendment review -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-21

The amendment review accepted the changed summary rule with no blocking finding. Its five non-blocking findings are taken, each with its own exact words (block R); status is now `ready-to-implement`.

1. N1 (a model's text quoting another run's frame): taken, Limits (6).
2. N2 (the pattern runs on each string on its own; the unmatched forms get tests): taken, Detail D3.2 and four more inputs in the D5 row.
3. N3 (the row's key set is not pinned): taken, Detail D4.
4. N4 and the reviewer's question (a separate work folder, or move the version change into C1): the first. The chunks are built in a work folder of their own and merged into `0.9-dev` together; Sequence says so.
5. N5 (C2's sentence; the list holds names that are not field names): taken, C2 and Detail D6. The rule sentence now says "names" where the accepted proposal said "field names". It binds every name, so nothing weakens.

Edited directly by Strategy, by exact replacement. Not run: any test, log read or meter run.

**Elapsed**: unknown. **Tokens**: unknown.
