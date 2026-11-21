# Count Claude usage toward a project

**Author**: Claude (Strategy), drafted by Claude Sonnet 5.5 (`claude-sonnet-5-5`)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy — it changes what the meter accepts as proof that usage belongs to a project
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: `dev/rules/working-agreements.md`, `dev/rules/conventions.md`, `dev/rules/custom_session_routines.md`
**In brief**: The usage meter would count Claude's own token use toward a project, using the working folder each Claude record names, so the end-of-session report stops showing it as unknown.

## Decision summary

**Conclusion.** Let the meter count Claude usage, sub-agents included. Antigravity gets a look only, with your leave.

**The problem.** You asked for cost data "so we can actually see what works to keep costs down." The end-of-session report shows Claude usage as unknown. The hand-kept cost record measured the wrong thing: the figure the tool gives for each sub-agent is close to the size of its last request, about a thirtieth of what the sub-agents used that day. Two thirds of that day's tokens were the coordinating session's own, which the hand record cannot see (both measured 2026-11-21). Only the tool's logs hold real use. The meter reads them but will not accept the folder a log sits in as proof of the project. You decided (chat, 2026-11-20): "Yes, both CLAUDE and Antigravity should count."

**What is added.**
- A Claude record counts toward a project when its working folder is the project's or inside it, its log is under a folder you approved, and the project's Git remote (the address of its shared repository) checks out as for Codex. All 3,434 records measured carry that folder.
- Sub-agent transcripts count the same way. The one-line summaries in the main log are not usage.
- The report shows Claude usage for the project by kind of token: fresh input, cache writes, cache reads and output.
- One rule sentence on what may leave a provider log: counts, the meter's own cleaned output, and field names from a list kept beside the rule.

**What it costs.** Anything that can write files as you, including the agents being measured, can add made-up Claude usage to a project; Codex logs can be forged the same way. The harm is a wrong number in the usage report and the project's export. Folders inside the project are new: 59 of 3,434 records came from one. A new reader version makes the meter refuse the ledger it holds (its private running record), so the first refresh fails until that ledger is rebuilt from logs still on disk; usage whose logs were deleted is lost. Yes or no is your call (choice 5).

**Not known.** Whether Antigravity's saved files hold token counts: a look at three transcripts on 2026-11-04 found none, and nothing has been looked at since. Whether a resumed session copies earlier messages under a new session id: such messages would become unknown, never counted twice, and a count-only measurement before the plan says how many. Whether a summary ties to its transcript by an id: if none does, a session that resumed a sub-agent prints as incomplete, as the measured one would (75 summaries, 70 transcripts).

**Five choices** (my pick first):
1. *Antigravity.* (a) One count-only look first, with your leave. (b) Build a collector for its live status line now: larger, and a new place where Cairn writes. (c) Leave it out, with the reason shown.
2. *Folders inside the project.* (a) They count. (b) Only the exact path counts, as for Codex.
3. *A table for each agent run*, one row for each sub-agent with its real use. (a) Not now. (b) Include it now.
4. *When.* (a) v0.9, so issue #96 closes with this release. (b) v0.10.
5. *The ledger the meter holds.* (a) Rebuild it from the logs still on disk at the first refresh. (b) Keep the old one readable: more code.

## Context

The meter (`dev/tools/meter.py`) reads only source folders named in the user's consent file. Its Claude reader marks each assistant event `project_path_unapproved`, ownership unknown. The project export keeps only events with a verified project and proven ownership (`_project_export`), so none reaches a project.

Codex differs: `read_records` sets a project when the record's folder equals exactly one configured project path, then checks the project's Git remote (`_verified_project_remote`). Plan C's check on a real log found one case left: a sub-agent summary in an `attachment` record trips `unsupported_record`. Plan C's Security Review required flagging a `usage` key at any depth and exempting no record by type name.

**Measured 2026-11-21, counts only, one session** (`dev/PLANNING.md`, "The rest of #96"):
- 3,434 assistant records in the session log and 4,947 in 70 sub-agent transcripts. Each has a working folder, session id and request id; every folder was the project's root or inside it.
- Transcripts sit beside the session log, carry the parent's session id and a side-chain mark, and share no message with it.
- 75 summaries in the session log; 70 have totals within one percent of a transcript's last request.
- 3,806 messages in the log and transcripts together (the cost record's table shows 3,755, counted earlier that day; the session had grown). 3,130 are written on more than one record, and in every one the repeats carry equal usage. No assistant record lacks a request id.

**Read from the code, not measured.** The scanner descends sub-folders to depth 32 (`_enumerate_jsonl`), so transcripts under an approved root are already read. An event key is session, request id and message id. Records with one key and equal usage merge; unequal usage makes the event unknown (`conflicting_usage`).

## Proposal

**A. A Claude record proves its own project.** It counts toward a configured project when all three hold; otherwise it stays unknown, with a reason.
1. Its log lies under an approved source root, as today.
2. Its working folder, compared as text and never opened, is the project's path or lies inside it, for exactly one configured project. The folder is the record's own `cwd` text. It must be absolute, hold no `.` or `..` part and no control character, and on Windows use a drive letter and backslashes only (no `/`, and no network-share prefix of two backslashes), as the Codex check requires; otherwise the record stays unknown with `project_path_unapproved`. It is compared with the configured path as the config file stores it, with no case folding, no trailing-separator trimming, no `..` resolution and no symlink or drive-mapping lookup: a differing letter case or a trailing separator makes it unknown. It counts as inside the project only when it equals the project path or begins with the project path followed by one separator (a backslash on Windows, `/` elsewhere), with no empty part after it, so `/w/cairn-old` is not inside `/w/cairn`. A folder inside two configured projects (one nested in the other) counts for neither.
3. The project's Git remote passes the Codex check, which reads the configured project's own `.git/config`.

The log's folder is never proof. A record with no request id stays unknown, and a test with a configured project pins it. Ownership becomes proven only on a record passing all three. A Claude event is keyed by its request id and message id, not its session. A message seen under two session ids, or with two folders, becomes unknown with `conflicting_binding` and never counts twice; the count-only measurement before the plan reports how many messages that affects. A folder link inside the project counts as inside: an accepted limit, since the folder is compared as text and never opened.

**B. Sub-agent transcripts are usage and count under A; their summaries are not.** Equal repeats already merge by event key, and in the measured session every repeat was equal. A record is a summary only if every `usage` key found in it (anywhere, as `_record_carries_usage` walks) is a dict with exactly the three fields the plan names from the measured record, each a non-negative whole number and not a boolean. The meter does not count a summary and does not call it unsupported. For Claude, a record that carries `usage` and is neither an assistant record nor a summary gets the new reason code below, not `unsupported_record`. Records of the four types the reader already skips (`user`, `system`, `progress`, `file-history-snapshot`) stay skipped; a test pins that. The reading is marked incomplete, with a new reason code kept off `_PULSE_BENIGN_REASONS` (`dev/tools/pulse.py`), when for any session the summaries outnumber the distinct sub-agent transcripts read under approved roots. It compares counts because no id is yet known to tie a summary to its transcript; if the measurement before the plan finds one, the plan matches by id. The ledger keeps, for each session, the summaries and distinct transcripts seen across refreshes; while summaries outnumber transcripts, or the new reason is present, it is in every project export's coverage reasons, so the report prints INCOMPLETE.

**C. The report shows it.** `pulse.py` marks a tool PARTIAL when the aggregate has rows for it, so Claude rows appear and no report format changes. I found no pinned test expecting a matching Claude record to stay unknown; I did not read all of `tests/integration/test_meter.py`. The usage-free tests gain a summary case.

**D. Antigravity: look before building.** The reader is a deliberate stub; this proposal builds none. It asks your leave for one count-only look at Antigravity's saved files where you use it: field names from a fixed list, and counts; nothing copied. If they hold token counts and a working folder, a follow-up plan adds a reader under A's rule. If not, the report says why and that part of #96 closes on that reason with your word.

**E. The rule is written down.** One sentence in `dev/rules/custom_session_routines.md`, beside the consent rule: nothing read from a provider log goes into a plan, test, fixture, commit, report, chat reply or agent prompt except counts, the meter's own sanitized output, and field names on the list kept in this file; any other field name is counted, never shown. The list is fixed because on 2026-11-21 a count-only check printed a sentence: a record used one as a field name.

**Not here.** A table for each agent run (choice 3); a collector for Antigravity's live status line; usage kept under another field name than `usage`, which stays unseen.

**Ledger cost.** A new `READER_VERSION` makes `_load_ledger` refuse the ledger the meter holds, so the first refresh fails until that ledger is rebuilt from logs still on disk; usage whose logs were deleted is lost (choice 5). Earlier Claude events are not back-filled.

## Rationale

The record names its own project, as Codex's does: one trust story, one difference.

## Alternatives considered

- **Do nothing.** Claude stays unknown.
- **Trust the log's folder.** It names the tool, not the project.
- **Count the summaries.** Each is about one request's size.
- **Exempt `attachment` by type name.** Plan C's Security Review rejected it.

## Documentation / doctrine surface

`dev/rules/custom_session_routines.md` (E); `dev/measurement/README.md`; `dev/PLANNING.md`; the changelog.

## Evidence / verification plan

Tests use hand-written records. Failing cases: a folder outside every project; inside two; a failed remote check; repeats with differing usage; a summary with no transcript; another non-assistant record with `usage`. **One developmental check on a real log, with your leave:** the meter's Claude totals for one session, by kind of token, equal an independent count-only sum of its log and transcripts. **To be measured before the plan, counts only:** whether a summary ties to its transcript by an id; how many messages appear under two session ids, as a resumed session might write them; how many records' folder text equals the configured path exactly, letter case included; and whether any record of the four skipped types holds a summary. The drafting agent ran no test and read no log.

### Security preflight

- **S1** Log files under approved roots. A record's folder and ids are data, compared as text, never opened. Project path and remote come from the consent file.
- **S2** Each failing case above leaves usage unknown or the reading incomplete.
- **S3** The user's own `refresh` command, over approved roots and configured projects only.
- **S4** Toward unknown or incomplete, never a guessed number.
- **S5** Forged logs; usage under another field name; a renamed field in a new tool version; logs deleted before a refresh; the measured agents themselves write under approved roots; a tool version changes the summary shape.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

- Totals that differ from the independent sum.
- A project showing usage from work done elsewhere.
- A reading called whole when transcripts were missing.

## Scope delta

**Scope delta**: degraded -- Antigravity counting. **Disposition**: defer, until choice 1 is answered. The Maintainer's word was that both tools should count; this proposal delivers a look only for Antigravity.

## Assurance path

**Assurance path**: high-assurance

## Review -- Claude Sonnet 5.5 (`claude-sonnet-5-5`) -- 2026-11-21

```
Reviewed commit: 1c084176f4e664bbe718c56a3838b86a9b523a72
```

**Tier**: usual
**Findings**: raised (4 blocking, 5 non-blocking)
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes: a Claude record names its folder, as a Codex record does, and the folder a log sits in is no proof; the design is sound but four statements are not yet plannable -- `dev/tools/meter.py` lines 6659 and 6829-6832.
2. **Best alternative.** Do nothing leaves Claude at UNKNOWN, which the Maintainer's quoted word rejects; counting only the exact path (choice 2b) is the safer fallback and is offered -- `dev/tools/pulse.py` line 815.
3. **What would show it wrong.** A count-only sum of one session that differs from the meter's total, or a session reported whole with summaries outnumbering transcripts: 75 summaries against 70 transcripts in the measured session -- `dev/measurement/agent-step-costs.md` line 203.

The proposal's aim holds up: read the record's own folder, never the log's, so cost data stops depending on a hand-kept record that measured the wrong thing. Most statements about the code are true: the Codex rule is exact string equality (6829-6832), `_enumerate_jsonl` descends sub-folders, repeats with unequal usage become `conflicting_usage`, and `pulse.py` marks PARTIAL on any aggregate row.

**Blocking**

1. **Outcome A's folder rule is left to the plan's author.** Add to A.2 the exact words in block 1 below.
2. **Outcome B's incomplete rule misses the case measured.** "Summaries and no transcript at all" would print the measured session whole with 5 of 75 runs missing. Replace with block 2.
3. **Outcome B states something false and leaves the shape undefined.** "Any other non-assistant record carrying `usage` stays `unsupported_record`" is not true of `user`, `system`, `progress` and `file-history-snapshot`, which are skipped before the check (6625-6628). The shape's field names and place are also not given. Replace with block 3.
4. **The Decision summary omits the ledger effect.** A changed `READER_VERSION` makes `_load_ledger` raise (3042), so the first refresh fails until the old ledger is rebuilt. Add the sentence in block 4 under "What it costs".

**Non-blocking**

5. The request-less sentence (A, last paragraph) cites a test that runs with no configuration, so it pins nothing about the new rule; and today a request-less record falls back to its message id (6633). Say "stays unknown, and a test with a configured project pins it."
6. A message whose repeats carry different folders already becomes `conflicting_binding` (7099); say so.
7. Resumed sessions: measure before the plan, as the summary already promises for summaries; list it under the evidence plan. A log under two roots merges by event key, so it counts once.
8. The summary leaves "table for each agent run", "kind of token" and "Git remote" undefined; the proposal's 3,806 messages differ from the cost record's 3,755 (the session grew?). Say which.
9. Antigravity: the Maintainer's word was "both should count"; the proposal delivers a look only. Write **Scope delta**: degraded -- Antigravity counting, **disposition**: defer until choice 1 is answered.

Tier heavy and the plan review are right. Not covered: I ran no test, read no log, and judged the summary as prose only; the Security Review owns S1 to S5 and the trust question for "proven".

### Exact words

1. After A.2's sentence, add: "The folder is the record's own `cwd` text. It must be absolute, hold no `.` or `..` part and no control character, and on Windows use a drive letter and backslashes only (no `/`, no `\\\\` prefix), as the Codex check requires; otherwise the record stays unknown with `project_path_unapproved`. It is compared with the configured path as the config file stores it, with no case folding, no trailing-separator trimming, no `..` resolution and no symlink or drive-mapping lookup: a differing letter case or a trailing separator makes it unknown. It counts as inside the project only when it equals the project path or begins with the project path followed by one separator (`/` or `\\`), so `/w/cairn-old` is not inside `/w/cairn`. A folder inside two configured projects (one nested in the other) counts for neither."
2. Replace B's last sentence with: "The reading is marked incomplete, with a new reason code kept off `_PULSE_BENIGN_REASONS`, when for any session the summaries outnumber the distinct sub-agent transcripts read under approved roots. It compares counts because no id is yet known to tie a summary to its transcript; if the measurement before the plan finds one, the plan matches by id. Recomputed from the files on disk at each refresh, never kept as whole."
3. Replace B's third sentence with: "A record is a summary only if every `usage` key found in it (anywhere, as `_record_carries_usage` walks) is a dict with exactly the three fields the plan names from the measured record, each a non-negative whole number and not a boolean. Any other `usage` key makes the record `unsupported_record`. Records of the four types the reader already skips (`user`, `system`, `progress`, `file-history-snapshot`) stay skipped; a test pins that, and the Security Review judges it."
4. Under "What it costs": "A new reader version makes the meter refuse the ledger it holds, so the first refresh fails until that ledger is rebuilt from logs still on disk; usage whose logs were deleted is lost. Yes or no is your call (choice 5)."

## Review -- Claude Opus 5.5 (`claude-opus-5-5`) -- 2026-11-21

```
Reviewed commit: b99c636d48e7f2c5c37ff5dbce1f3caa4596f6a7
```

**Tier**: Security Review
**Findings**: raised (3 blocking, 4 non-blocking)
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes, if "proven" stays honest: a Claude record's only proof is its own folder text, while a Codex record must also agree with its session header, its copy and fork checks and the remote that header recorded -- `dev/tools/meter.py` lines 6796-6824 and 7055.
2. **Best alternative.** Choice 2b (exact path only) narrows which folders count but adds no proof; the stronger fix is keying on the provider's ids so copies cannot count twice -- `dev/tools/meter.py` line 6634.
3. **What would show it wrong.** One message counted under two session ids, or a report printed whole after a summary changed shape -- `dev/tools/pulse.py` line 39 (`unsupported_record` is harmless).

The proposal's aim is right: count real use from the record's own folder, never the log's, and fail toward unknown. Three gaps break that promise.

**Agreement with the usual review.** Its blocking 1, 3 and 4 hold. Blocking 2 holds, but my block S2 governs its last sentence: Claude logs are read incrementally, so "recomputed from the files on disk" cannot be built. In its block 1, replace "(`/` or `\\`)" with "(`\` on Windows, `/` elsewhere), with no empty part after it": the configured path is stored as Python's `Path` text (lines 1072-1077).

**Blocking**

S1. **"Proven" lacks a copy check, and the cost line is wrong.** The event key includes the session (6634); a resumed or forked session that copies messages under a new id counts them twice, breaking S2 and S4. Codex logs can be forged as easily; what Claude lacks is Codex's copy and fork checks. Use block S1.
S2. **A changed summary shape hides missing transcripts.** A summary that fails the shape becomes `unsupported_record`, which the report treats as harmless; it is then not counted as a summary, so the incomplete rule never fires. Use block S2.
S3. **Outcome E is ambiguous.** It forbids the meter's own export (model names come from logs), does not cover chat or agent prompts, and names no home for the list. Use block S3.

**Non-blocking**

S4. A folder link inside the project counts as inside; state it as an accepted limit in A.
S5. Add to S5: "the measured agents themselves write under approved roots; a tool version changes the summary shape."
S6. The four skipped types cannot add usage; keeping them skipped is acceptable if the measurement before the plan finds no summary in them.
S7. Reading question: E adds a rule; none weakens.

Not covered: I ran no test, read no log, did not read the Antigravity or Codex tests or Plan C's companion, and did not trace how a reader reason reaches the project export.

### Exact words (Security Review)

S1. In "What it costs", replace its first two sentences with: "Anything that can write files as you, including the agents being measured, can add made-up Claude usage to a project; Codex logs can be forged the same way. The harm is a wrong number in the usage report and the project's export." In A, after "Ownership becomes proven only on a record passing all three.", add: "A Claude event is keyed by its request id and message id, not its session. A message seen under two session ids, or with two folders, becomes unknown with `conflicting_binding` and never counts twice; the count-only measurement before the plan reports how many messages that affects."

S2. In B, after the summary-shape sentence, add: "For Claude, a record that carries `usage` and is neither an assistant record nor a summary gets the new reason code, not `unsupported_record`." Replace the usual review's "Recomputed from the files on disk at each refresh, never kept as whole." with: "The ledger keeps, for each session, the summaries and distinct transcripts seen across refreshes; while summaries outnumber transcripts, or the new reason is present, it is in every project export's coverage reasons, so the report prints INCOMPLETE."

S3. Replace E's quoted rule with: "Nothing read from a provider log goes into a plan, test, fixture, commit, report, chat reply or agent prompt except counts, the meter's own sanitized output, and field names on the list kept in this file; any other field name is counted, never shown."

## Response -- Claude Fable 5.2 (Strategy, author of the design) -- 2026-11-21

Both reviews said revise. All seven blocking findings came with the words that close them; all are accepted and folded into the text above, and nothing is declined.

Usual review:

- **1, the folder rule was left to the plan: closed.** A.2 carries its words, with the Security Review's correction that the separator is the host's own. The network-share prefix is named in words, to avoid a doubt about how many backslashes were meant.
- **2, the incomplete rule missed the measured case: closed.** B marks a reading incomplete when summaries outnumber transcripts; the Security Review's sentence governs how that is kept across refreshes.
- **3, a false statement and an undefined shape: closed.** B defines a summary by every `usage` key in the record. Where the two reviews differ on a record that is neither, the Security Review governs: it gets the new reason code, so the report cannot pass it as harmless.
- **4, the ledger effect: closed.** It is in the summary's costs and is choice 5.
- **5 to 9: accepted.** The request-less sentence no longer leans on a test that pins nothing; two folders on one message is named; the measurements owed before the plan are listed under evidence; three terms are explained in the summary and the two message counts reconciled; the scope delta is stated as degraded for Antigravity.

Security Review:

- **S1, copies counted twice: closed.** A Claude event is keyed by request id and message id. The reviewer asked whether a message seen under two session ids should become unknown or count once under the earlier session. It becomes unknown: that fails the safe way and needs no trust in a log's own times. If the measurement shows many such messages, the plan returns to this.
- **S2, a changed summary shape hid missing transcripts: closed** (B).
- **S3, outcome E was ambiguous: closed**, with its words.
- **S4 to S7: accepted.** The link inside a project is a stated limit; two entries join S5; the skipped types are checked in the measurement.

One consequence the folded text makes visible, my reading and not measured: the five summaries without a transcript in the measured session are probably sub-agents that were resumed, which leaves a second summary and one transcript. If no id ties a summary to its transcript, every such session will print as incomplete. The summary's "Not known" says so.

Also changed by me before review: one measurement, that repeats of a message always carried equal usage.

Not checked by anyone: Antigravity's files; a resumed session's log; a run of the changed meter on a real log, which waits for the Maintainer's leave.

**Elapsed**: unknown. **Tokens**: unknown.

## Decision -- Maintainer (scribed by Claude Fable 5.2) -- 2026-11-21

**Tier**: heavy

**ACCEPTED.** Asked "Usage-counting proposal (heavy tier): let the meter count Claude usage toward a project, sub-agents included. My picks: Antigravity gets a count-only look first, on your Mac with the re-anchor; work folders inside the project count; no per-run table for now; build it in v0.9 so issue #96 closes; rebuild the meter's ledger from the logs still on disk. Do you accept it?", the Maintainer chose, from the answers offered (2026-11-21):

> "Accept, your picks (Recommended)"

Just before, about the Antigravity part, he had written (chat, 2026-11-21):

> "I don't have Antigravity on this machine--it's on my Mac. Can we implement this there later? Along with that reanchor?"

What that settles:

- **Choice 1: (a).** One count-only look at Antigravity's saved files first. It happens on his Mac, in the session that runs the re-anchor, and nothing is built for Antigravity before it.
- **Choice 2: (a).** A record from a work folder inside the project counts.
- **Choice 3: (a).** No table for each agent run for now.
- **Choice 4: (a).** Built in v0.9.
- **Choice 5: (a).** The meter's ledger is rebuilt from the logs still on disk.
- **Tier.** Heavy, as proposed.

**Elapsed**: unknown. **Tokens**: unknown.

## Decision, release and scope -- Maintainer (scribed by Claude Fable 5.2) -- 2026-11-21

**Changed: the release that carries this work, and when Antigravity is built.** The Maintainer had written that the defect fixes will be cut as v0.8.1. Strategy then asked "Is counting Claude usage part of v0.8.1?" and recommended that it ship in v0.9. He wrote (chat, 2026-11-21):

> "Yes. Claude and Antigravity are part of v0.8.1. Excluding them was a defect. I use all three every day. The same way that excluding Windows and Linux certification was a defect."

What that settles:

- **Choice 4 is now v0.8.1.** Counting Claude usage is built for the defect-fix release, not for v0.9.
- **Antigravity is part of v0.8.1 too.** Choice 1 (a) stands as the order of work: one count-only look at Antigravity's saved files comes first, on his Mac, and a reader is planned from what the look finds. What changes is that this happens before v0.8.1 is cut.
- **Choices 2 and 3 stand.** Choice 5 stands under the question recorded on the roadmap: the meter cannot rebuild its record from old logs, and whether the restart is accepted is still his to say.

**Elapsed**: unknown. **Tokens**: unknown.
