# Plan: Count Claude usage toward a project

**Source proposal**: dev/proposals/archive/2026-11-21-claude-usage-counting.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/custom_session_routines.md, dev/rules/protected-surfaces.md, dev/rules/development-environment.md
**In brief**: The usage meter counts Claude's own token use toward a project, by the working folder each Claude record names, so the end-of-session report stops showing Claude usage as unknown.

## Build summary

After this plan the meter counts a Claude record toward a project when the record's own working folder is the project's or inside it, its log sits under a folder the Maintainer approved, and the project's Git remote checks out. Sub-agent transcripts count the same way. Summaries of finished sub-agents are not counted; a reading whose summaries cannot be tied to a transcript prints INCOMPLETE. The meter's private ledger gets a new version, so the first refresh refuses the old one until it is moved aside. One rule sentence and a list of field names that may be shown go beside the consent rule. Only the existing meter and its tests change, in five chunks.

## Source proposal

The Maintainer accepted the proposal at the heavy tier on 2026-11-21 with all five of Strategy's picks: the Antigravity look happens later on his Mac; a record from a work folder inside the project counts; no table for each agent run; built in v0.9; the meter's ledger is rebuilt from the logs still on disk. The plan executes it and reopens nothing. Antigravity is not in this plan. Exact names, conditions and test inputs are in the companion `dev/plans/2026-11-21-claude-usage-counting-detail.md` ("Detail", D0 to D7), part of this plan; it exists so the opening text stays short and a low-tier agent invents no design.

## Scope

**Result.** The Pulse shows Claude usage for the project by kind of token (fresh input, cache writes, cache reads, output), with cost data that no longer depends on a hand-kept record that measured the wrong thing.

Proposed paths:
- `tests/test_meter_claude_usage.py`

**Measured by Strategy on 2026-11-21, counts only, one project's logs** (90 log files, 9,609 assistant records with usage): 4,333 distinct messages, none under more than one session id. No record of the four skipped types held a `usage` key. The folder equalled the configured project path exactly in 3,539 records and lay exactly inside it in 59; none differed only by letter case or separators, none lay outside. There were 84 summaries and 89 sub-agent transcripts; no summary's own id equalled a transcript's agent id, but the text of every one of the 84 names exactly one transcript's agent id. The incomplete rule below rests on that: a summary is covered when its text names exactly one agent id for which a transcript was read; one that names none, more than one, or an id with no transcript makes the reading incomplete. This leans on the tool's wording; a tool version that changes it turns readings incomplete, never whole.

**Why code, not written steps** (the Maintainer, 2026-11-21: "no new tooling unless it's needed"). Nothing new is a script or an option. Each piece added to the meter, with its reason:
- The folder rule (`_project_for_folder`): the text of every record's folder must be compared the same exact way thousands of times, and an agent following steps would miss a case.
- The Claude branch's proof of ownership: whether a record counts is decided by the code that counts, so the same record gets the same answer.
- The summary test (`_usage_values`, `_summary_names`): a record is a summary only on an exact shape, and any other record carrying `usage` must never pass as harmless.
- The ledger's memory (`agent_runs`): logs are read in pieces over many refreshes, so no one pass sees a summary and its transcript, and the count that links them must survive between runs.
- The version change: the meter already refuses an old ledger by this rule.

The rule sentence, the field-name list, the README and the changelog are written steps, not code.

**Limits stated.** (1) A folder link inside the project counts as inside, since the folder is compared as text. (2) A message seen under two folders or two sessions becomes unknown in one reading, and across refreshes when both folders map to a project; a repeat across refreshes where one folder lies outside every project is not caught. That is a narrower catch than the proposal's words, so reviewers decide whether it is a reduction. (3) Past 1,000 uncovered summaries or 100,000 transcripts, the meter cuts the excess and prints INCOMPLETE; it never fails a refresh over it. (4) The summary's three field names and the keys `isSidechain` and `agentId` were confirmed by Strategy on 2026-11-21 (Detail D7, P1 to P3). The author's first guess at the three names was wrong, and Detail D0 now holds the confirmed ones; they hold for the tool version measured. (5) The incomplete rule sees only summaries, and on the measured logs all 85 were in the main log: none was in a transcript, and ten of the 90 transcripts were named by no summary. By Strategy's reading those ten include runs that another agent started. Such a run is counted from its transcript like any other, but if its transcript were missing, nothing would mark the reading incomplete.

**Reuse.** The Codex project check (`_verified_project_remote`, the `verify_project` closure) and `_event_record` are reused as they are; the merge at the end of `read_records` already turns two bindings of one message into `conflicting_binding`. `_record_carries_usage` is replaced by `_usage_values`, the same walk, rather than a second walker. The Codex folder test is repeated in four lines, not shared, because the Codex tests pin `_codex_context`. Searched `dev/tools/` and `templates/skills/_lib/` for `cwd`, `isSidechain` and `usage`: only `meter.py` holds them.

**Doctrine surface.** `dev/rules/custom_session_routines.md` (one sentence and one list), `dev/measurement/README.md`, `CHANGELOG.md`. `dev/PLANNING.md` only has its two links to the proposal repointed.

**Stale records, and who refreshes each.** (a) `tests/fixtures/gate_manifest.json` holds a hash for `tests/integration/test_meter.py`, which this plan edits: it adds one line to the Maintainer's one signing, and no agent edits it. The other test files touched are not in that manifest (searched by name, 2026-11-21). (b) Cairn's own lock records the hash of `dev/tools/meter.py`: C5 refreshes it with the installer's scoped finalize over that file alone, in a commit that holds nothing else, then `install/verify_integrity.py --target .` must report OK. (c) The two meter copies must stay byte-identical: each code chunk copies and runs `cmp`; `tests/test_skills_install.py` and `tests/test_skills_upgrade.py` also check the copy. (d) No installer symbol changes, so no AST listing is owed.

## Sequence

C1 to C3 each end in the copy and `cmp`, one commit for each chunk, explicit paths only. The execution agents are Haiku; the plan's agent checks each diff against the criterion.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Folder proof, request key | plan review | `_project_for_folder`, the changed Claude branch, new test file and its tier entry |
| C2 | Summaries and transcripts | C1; Strategy's P1 to P3 | `_usage_values`, `_summary_names`, the batch's `agent_runs`, new reason |
| C3 | Ledger memory, versions | C2 | `agent_runs` in the ledger, coverage reason, `/6` versions, end-to-end tests |
| C4 | Rule and docs | C3 | rule sentence and list, README, changelog |
| C5 | Lock and joined run | C4 | refreshed lock, selection run and record |

## Acceptance criteria

**C1.** A Claude record whose `cwd` equals the project path or lies inside it, with a request id and a passing remote check, reads as `proven` and `current_local_verified`, with the project's alias. Each failing case in Detail D5 (outside, sibling name, trailing separator, other letter case, `..`, inside two projects, the Windows forms, failed remote check, unapproved root, no request id) stays unknown with its reason and has a passing control. One message under two sessions or two folders is one unknown event with `conflicting_binding`; equal repeats merge; differing usage gives `conflicting_usage`. Public entry: `meter.read_records`.

**C2.** A record with exactly the three summary fields is no event and leaves one summary row. Any other non-assistant, non-skipped record carrying `usage` adds `agent_runs_incomplete`, never `unsupported_record`; the four skipped types stay skipped whatever they hold. A sub-agent transcript record leaves one pair of keys. Each shape failure in Detail D5 has its control.

**C3.** After a refresh that reads a summary with no transcript, the export lists `agent_runs_incomplete` and the pulse prints INCOMPLETE; after one that reads the transcript, it does not. Another session's transcript, two named transcripts, or none leave it on; a record that could not be classified keeps it until the ledger is replaced. The ledger round-trips, each hand edit in Detail D5 is refused as `ledger_invalid`, and a `/5` ledger is refused with `ledger_old_schema` and left unchanged. Entries: `_refresh_ledger`, `_new_ledger`, `_load_ledger`, `pulse._parse_meter_aggregate`. End-to-end tests run on POSIX only (the Linux subsystem here).

**C4.** The rule sentence (Detail D6) is in `dev/rules/custom_session_routines.md` beside the consent rule, with the list of field names; the README and the changelog say what Detail D6 says. `python dev/tools/claim_check.py`, `link_check.py` and `tests/check_cairn.py` pass on each file.

**C5.** The lock is refreshed alone; `verify_integrity` reports OK; `cmp` of the two meter copies prints nothing; the nine selected files give no failure that is not the host's (compared before and after, Verification).

**Strategy's checks, not the build agent's** (they read private logs; the build agent must not attempt them). Before C2: P1 to P3 (Detail D7), which Strategy ran on 2026-11-21. After C3 and before code review: the proposal's developmental check, that the meter's Claude totals for one session, by kind of token, equal an independent count-only sum of its log and transcripts; it needs the old ledger moved aside first (choice 5), a first refresh to set the start, and a session written after it.

**Security (re-answered).** S1: input is log lines under approved roots; folders and ids are text, never opened; project paths and remotes come from the consent file. S2: each case in C1 to C3, with controls, leaves usage unknown or the reading incomplete. S3: the user's own `refresh`, over approved roots and configured projects. S4: it breaks toward unknown or INCOMPLETE, never a guessed number. S5: made-up usage written by anything that can write files as the user, the measured agents included, as for Codex (a wrong number in the report and export); a tool version that changes the summary shape makes readings incomplete; usage under another field name stays unseen.

## Scope delta

**Scope delta**: degraded -- Antigravity counting. **disposition**: defer. The accepted proposal assigns it: its choice 1 (a), one count-only look first. The Maintainer's Decision (2026-11-21) chose that, saying: "I don't have Antigravity on this machine--it's on my Mac. Can we implement this there later? Along with that reanchor?" Home: the Mac session's fourth job, in `dev/PLANNING.md` under "Waiting on you". Nothing else is cut.

## Verification

Changed promises: which Claude records count toward a project; summaries are not usage; a reading with untied summaries is INCOMPLETE; the ledger version. Entry points: `meter.read_records`, `_refresh_ledger`, `_load_ledger`, the pulse's reading of the export.

Test selection: `python tests/tier_inventory.py for dev/tools/meter.py templates/skills/_lib/meter.py` gave nine files on 2026-11-21. Chunks C1 to C3 run four of them plus the new file, which guard the changed promises: `tests/integration/test_meter.py`, `tests/test_meter_usage_free_records.py`, `tests/test_skills_install.py`, `tests/test_skills_upgrade.py` and the new `tests/test_meter_claude_usage.py` (listed in `tests/test_tiers.json` in C1, then `python tests/tier_inventory.py check`). C5 runs all nine once; the five not run earlier are `tests/security/test_git_read_routes.py`, `tests/test_security_lint.py`, `tests/test_session_failsafe.py`, `tests/test_session_routines.py` and `tests/test_session_writes_contained.py`. The Windows Server host fails many tests before any change, so each group runs once at the starting commit and once after, failing ids and messages are compared, and an id failing only after is rerun alone at both. POSIX-only tests run in the Linux subsystem, one run at a time.

Not run by the build agent: the real-log checks above. The broad selection, the Python 3.13 run and the joined run belong to the arc (`dev/PLANNING.md`, "What the joined run owes"). Prose gates (`claim_check`, `link_check`, `check_cairn`, `git diff --check`) run on every document changed.
