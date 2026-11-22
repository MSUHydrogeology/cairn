# Plan: Antigravity usage counts toward a project

**Source proposal**: dev/proposals/archive/2026-11-21-claude-usage-counting.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-22
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md, dev/rules/custom_session_routines.md
**In brief**: The usage meter will count Antigravity's token use toward a project, once per reply and tied to a conversation and a time, so its usage can be reported per project like Claude's and Codex's.

## Build summary

After this plan the meter counts Antigravity token use once per reply (the tool writes each record about four times) toward the one listed project that the conversation's own saved files name. A conversation that names none, or several, counts toward no project, and the report says so and labels the project figure as inferred. Each reply carries a one-way conversation fingerprint and a time, for the later cost-per-plan work. Counting starts only when the Maintainer adds Antigravity to his consent file; no agent does.

## Source proposal

The usage-counting proposal (heavy tier, accepted 2026-11-21) asked for one count-only look at Antigravity's files, and a reader only if they held token counts and a working folder. The look (`dev/measurement/antigravity-look-2026-11-22.md`) found token counts and a time on every record, but no folder. The Maintainer then wrote (chat, 2026-11-22):

> "We want Antigravity to function like everything else, and be able to measure for a plan. So do what's needed"

I read this as a project figure (not a machine-wide total, not left out) plus a run and a time on each reply: the look's option B, and the run identity the accepted cost-per-plan proposal (`dev/proposals/2026-11-22-claude-cost-per-plan.md`) waits for. He did not name option B; reviewers should test that reading. Cost per plan is not in this plan.

## Scope

**Result.** An Antigravity reply is counted once, with a conversation fingerprint and a time, toward the one listed project its conversation names, or toward none. "Listed" means named in the Maintainer's consent file.

**Measured by the look** (counts only, one Mac, one moment): 24,339 records hold both token fields and a text time, none a folder; 6,134 are distinct; 92 name a model; of 48 conversation folders, 40 name this project's root in their saved files and 5 name it and another folder. **Closed by a seventh count-only probe** (the Mac, 2026-11-22, at the Maintainer's word "do what's needed"; added to [the look's record](../measurement/antigravity-look-2026-11-22.md)): the time field is `created_at`, an ISO-8601 text with a time, in all 12,268 token records of `logs/`; none of those records names a model (`model`, `modelName` and `model_name` appear in 0 of 12,268; the look's 92 were in the `chunks/` copies, by subtraction), so every Antigravity reply's model is unknown; a token record names no conversation, so the run identity comes from the folder name; and each of the 6,134 keys appears exactly twice in `logs/`, so none appears four times and no collision was found. `created_at` joins the names list in `dev/rules/custom_session_routines.md` ("the keys the reader reads") in C3. Still unknown: whether `ANTIGRAVITY_TRAJECTORY_ID` equals the folder name.

**Rules.**
1. **Read set.** Only `*.jsonl` files directly inside `brain/<id>/.system_generated/logs/` under the consented root, `<id>` a canonical lowercase UUID; not `logs/chunks/`, which the look measured as repeats. A line is a reply only if it is a top-level JSON object with `input_tokens` and `output_tokens` as non-negative whole numbers (no booleans) and a zone-aware time in the named field. A line with neither token field is skipped, unless it holds a `usage` key at any depth, which gives `unsupported_usage_contract` (the stub's reason), so a format change shows. One field, a bad number or a bad time gives `invalid_record` and no event. A record naming a conversation id other than its folder's gives no event and `conflicting_binding`.
2. **Kinds.** Input is fresh input and output is output; both cache kinds are unknown (`None`, never 0), as Codex's absent cache-write is. I assume `input_tokens` may include cached text. The model is the record's own name if it passes `_safe_alias`, else unknown. `_weighted_reference_tokens` (3641) already gives no total when a kind or the model is unknown, so none is invented.
3. **Duplicates.** The key is a digest of tool, conversation, time, input and output; the existing merges join copies within a file, across files and across refreshes. One case goes wrong: two genuine replies alike in all four count once, an undercount. Accepted. The seventh probe counted the keys: 12,268 records for 6,134 keys in `logs/`, exactly two each. If each reply is written twice there (assumed), a collision would show as a key written four times; none did, so no collision was found in this data.
4. **Run identity** (one agent's stretch of work; here a conversation). Thread and session are the conversation id, stored only as `_digest("antigravity", id)` and `_short_session_digest(id)`, the helpers Claude's reader uses. The time is the record's. No raw id or path is stored or printed. Whether an agent can name that id when it declares a stage is for the cost-per-plan plan.
5. **Attribution (the trust change).** A conversation is the folder `brain/<id>/`. Searched: regular files up to 8 levels down ending `.txt`, `.md`, `.json`, `.jsonl` or `.log`, links skipped, read in 64 KiB blocks. A file names a project when the project's path text from the consent file occurs in it, exact case, with the byte before not a letter, digit, `.`, `_`, `-`, `~`, `%` or `/` (the literal `file://` excepted) and the byte after not a letter, digit, `.`, `_` or `-`. So `/a/cairn-old` does not name `/a/cairn`; a sentence-final period blocks a match, which fails toward unattributed; on Windows the doubled-backslash form counts too. Exactly one listed project named: the replies carry it (`current_local_verified` and `proven` here mean only that this rule held). None named: `antigravity_project_not_named`. Two or more, a listed project nested in another included: `antigravity_projects_ambiguous`. An unlisted folder named is ignored. Only which projects matched leaves the search.
   **Bounds** (my starting values, not measured): 16 MiB read and 5,000 entries per conversation; over, or an unreadable file, gives `antigravity_search_incomplete`, never a guess. A refresh stops searching at 256 MiB, also charged to the run's 1 GiB; conversations it cannot pay for wait for the next refresh (`catching_up`) with their logs unread. The search runs once per refresh for a conversation with new log bytes and stops at the second project named. An event keeps the project it was read under; seen later under another it becomes unknown (`conflicting_binding`, `_merge_retained_event`, 1814).
   **Weakness.** Text can name a folder for any reason. Anything that can write under `brain/<id>/` can move a conversation's tokens into a listed project, or out of all by naming two. The harm is a wrong number in a report; the attribution grants nothing and no gate reads it.
6. **Label and gaps.** Two coverage reasons, no new column or schema change. `_project_export` (2394) adds `antigravity_project_inferred` when its rows include tool `antigravity`; `_new_ledger` (3246) adds `antigravity_unattributed` when a project-less aggregate row has that tool. Unattributed tokens stay in the ledger's project-less rows (`_recompute_aggregates`, 1977), private; a project's export would misattribute them. Neither reason is on `_PULSE_BENIGN_REASONS`, so the pulse prints INCOMPLETE beside them with no `pulse.py` change; the cost is INCOMPLETE where nothing is missing (making the first benign is one line in `pulse.py` and its twin, the Maintainer's call). Rejected: a column like `model_provenance`, named on 40 lines of `meter.py` and 3 of `pulse.py` (row fields, 311), with a ledger schema bump and a second restart of a ledger restarted today.
7. **Reach and consent.** The consent file already accepts `antigravity` (`TOOLS`, 38; `validate_config_bytes`, 301). The Maintainer adds the source, root `~/.gemini/antigravity` written absolutely, himself or by a clear yes in chat; no agent creates or edits `~/.cairn/meter.json`. The generic walker `_enumerate_jsonl` (406) would also read `logs/chunks/`, and its 100,000-entry limit (176) fails the refresh for every tool; the look's 9,330 files left out program folders, so the real entry count is unknown. New `_enumerate_antigravity` instead builds every path from fixed names (`brain`, a UUID folder, `.system_generated`, `logs`) and listed entries, never from record text or `..`, skips links at every level, refuses a linked root (the refresh is then unavailable, as for a missing root today) and opens files without following. It never lists the root's parent, so the credential file in `~/.gemini/` is unreachable even from a misspelled root.

**Smallest build.** A branch in `read_records` (3878) replacing the stub (3979 to 3981), plus `_antigravity_usage` beside `_claude_usage` (3603), `_enumerate_antigravity`, `_antigravity_conversation` and `_conversation_project` beside `_enumerate_jsonl`, and constants `MAX_ATTRIBUTION_BYTES`, `MAX_ATTRIBUTION_ENTRIES`, `MAX_ATTRIBUTION_DEPTH` and `MAX_ATTRIBUTION_RUN_BYTES` near 175 to 195. Not a separate reader: that would copy what `read_records` ends with, the clear of a failed batch (4353 to 4367), the duplicate merge (4430 to 4526) and the return shape the scan reads (4555 to 4574), and forgetting one would count a torn batch. Claude and Codex lines stay untouched; shared edits are gated on the tool name. Changed: `read_records`'s signature (`attribution`, a dict of conversation id, project alias or `None`, and reason; without it no reply is read); `_scan_approved_sources` (2791) at 2813 (walker), 2910 to 2946 (find or defer the attribution, pass it) and 2951 (Antigravity always takes the start filter, since copies carry the original time; I do not know when copies are written); `_project_export`; `_new_ledger`. Unchanged: `READER_VERSION` and the ledger schema (an old ledger holds no Antigravity event; a new version would refuse it, 1652), `pulse.py`, the validators.

**Reuse.** `_digest`, `_short_session_digest`, `_event_record`, `_counter`, `_timestamp`, `_safe_alias`, `_is_link` and the Claude merge. Searched `meter.py` for `os.scandir` (one walker, which cannot be limited to `logs/`) and for any folder-text search (none). **Doctrine surface:** the names list in `dev/rules/custom_session_routines.md`; `dev/measurement/README.md` and `templates/core/dev/measurement/README.md` (not twins; both say the meter has no Antigravity reader); `CHANGELOG.md`. **Out of scope:** cost per plan, the live status line, protobuf and SQLite files, weighting Gemini replies, the Claude and Codex readers.

**Security preflight, what changes.** S1: file text under `brain/<id>/` is a new input, matched as bytes and never opened as a path. S2: the controls are C2's cases and C3's link and outside-path cases. S3: the Maintainer's `refresh` over listed sources only. S4 and S5: every failure leaves a conversation unattributed or a reply uncounted; forged text or logs are Claude's and Codex's class, and rule 5's weakness is the new residue.

## Sequence

Low-tier execution of an accepted plan; one commit per chunk by explicit path; each code chunk copies `dev/tools/meter.py` over `templates/skills/_lib/meter.py` and runs `cmp`. C3 also closes the board's wait on how Antigravity is attributed (`dev/PLANNING.md`) and adds W1 as a named wait, by exact replacement after a claim, and edits the names list as a deliberate rule change. One code review, usual and Security, follows C3.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Reader branch: dedupe, unknown kinds, run fingerprint | none (the probe is done) | the `read_records` branch, `_antigravity_usage`, two tests |
| C2 | Attribution and its bounds | C1 | `_conversation_project`, constants, one test |
| C3 | Wiring and records | C2 | walker, scan edits, two reasons, two tests, both READMEs, changelog, names list, board rows, lock |

**Owned wait W1, not a chunk.** The real-log check, a count-only comparison in the style of `dev/measurement/meter-mac-check-2026-11-22.md`. Owner: the Maintainer, who adds the source or says yes in chat. Restart: the source exists. Evidence: meter and an independent count agree on distinct replies and on input and output sums; attributed shares are set against the look (40 of 48 conversations); counts of cap hits and own-id mismatches. The plan reaches `ready-to-archive` without it; the real-log result stays unpassed until the record exists.

Proposed paths:
- dev/measurement/antigravity-meter-check-YYYY-MM-DD.md

## Acceptance criteria

**C1.** A valid line yields one event: input and output as read, both cache kinds `None`, the record's time, `session_key` equal to `meter._digest("antigravity", id)`, the model only if the record names one, no weighted total. The same record four times, and two records alike in conversation, time and counts, yield one event. Rule 1's failing lines yield none and a closed issue. The existing stub test passes unchanged. Entry: `meter.read_records`.

**C2.** A conversation naming exactly one listed project is attributed to it. Each of two projects named, none named, a longer name only (`<root>-old`), over the byte cap, and a link to an outside folder that names the project leaves it unattributed with rule 5's reason, and no case reads past the cap. Entry: a synthetic refresh.

**C3.** After a second refresh a reply appended to a conversation log counts once toward its project and the export holds `antigravity_project_inferred`; an unattributed conversation adds `antigravity_unattributed`. A `chunks/` copy, a linked log, a non-UUID folder and a file beside the root are never opened (an `os.open` spy sees only paths under the root). A copy older than the source's start is not counted. Claude and Codex tests pass unchanged. The two READMEs drop the no-reader sentence and state the label; the changelog extends the Major entry on Claude usage (a feature adopters notice, by the test at the top of `CHANGELOG.md`); the twins are byte-identical; the lock hashes of the changed hashed paths advance and `install/verify_integrity.py --target .` reports OK.

**Tests**, all in `tests/integration/test_meter.py`, synthetic folders only: C1 `test_antigravity_token_records_become_events_with_unknown_cache_kinds` and `test_antigravity_lines_that_are_not_complete_token_records_make_no_event`; C2 `test_an_antigravity_conversation_is_attributed_only_to_the_one_listed_project_its_files_name` (parameterized); C3 `test_an_antigravity_refresh_reads_only_conversation_logs_and_counts_each_reply_once` and `test_antigravity_attribution_shows_in_the_export_reasons`. The refresh tests mirror `test_a_link_out_of_a_log_folder_is_not_followed` (4558). Estimated time: about 1 minute for these nodes, then `tests/integration/test_meter.py` once at the end of C3 (366 cases took 2.7 s in the 2026-11-12 run; the file has grown and I did not re-measure). No other file runs, since `pulse.py` is unchanged.

## Scope delta

**Scope delta**: preserved. The accepted proposal's record reads "degraded -- Antigravity counting", disposition defer. This plan delivers that counting by the Maintainer's word above; nothing accepted is removed.

## Verification

Entries: `meter.py refresh` and `meter.read_records`. With `$HOME/conda_envs/lhm/bin/python3.13`: the named tests; `cmp` on the twins; the claim, link and `tests/check_cairn.py` gates on prose; `install/scaffold.py upgrade --finalize` for the changed hashed paths, then `install/verify_integrity.py --target .`.

**Protected files, checked 2026-11-22.** `tests/fixtures/protected_test_roster.json` names none of the touched files. `tests/fixtures/gate_manifest.json` pins `tests/integration/test_meter.py` (a SHA-256 under `ordinary_test_files`, already different from the file today, and 368 node ids, to which C1 to C3 add) and names `templates/skills/_lib/meter.py` only inside two node ids; it freezes no meter file, README or changelog. The Maintainer sees the test file at his next signing. The twin is a Python template, a high-risk surface, so the Security Review applies.

**Not checked.** I ran no test and read no Antigravity file or `~/.cairn/meter.json`. Unknown: the caps and depth, whether `input_tokens` includes cached text, Windows spellings of a folder in Antigravity's text, and whether `ANTIGRAVITY_TRAJECTORY_ID` equals the folder name. This plan runs about 2,400 words (`wc -w`) against a 1,500 target because it states a trust change and each limit in full.

## Plan review -- Claude Opus 5.5 (Security reviewer) -- 2026-11-22

Reviewed commit: 149606373bc17f885fe7fe8e1a72e2f5a8f3adeb (plan and `meter.py` unchanged at 5ba023b3)

**Obligation**: the Security Review of the trust change (rule 5) and its reach
**Tier**: Internal Security Review
**Findings**: raised (2 blocking, 4 non-blocking)

**Foundations**:

1. **Should this happen as framed?** Yes: option B is the reading of "function like everything else"; the harm of a wrong match is a wrong report figure -- plan rule 5; `_project_export` copies only counts (`meter.py` 2300-2408).
2. **Best alternative.** None simpler gives a project figure; the fixed-name walker is safer than `_enumerate_jsonl`, whose 100,000-entry cap fails every tool (406, 2814-2816).
3. **What would show it wrong.** Most conversations over the 16 MiB cap: 563 MB over 48 conversations averages 11.7 MB, so the caps may defeat the outcome; nobody has counted per-conversation size.

**Blocking**

B1. **S4 is false: a missed second name misattributes, it does not leave a conversation unattributed.** A synthetic check of rule 5's bytes gave `worked in /x/cairn and /x/cairn2.` -> `/x/cairn` only (period blocks `/x/cairn2`); also missed for the second project: `~`, case, NFD, `%20`, Windows `c:/`, and a name split across two 64 KiB blocks. A non-ASCII byte after the root (`/x/cairné`) wrongly matches `/x/cairn`. The prefix pair `/x/cairn`, `/x/cairn2` is correct. Rule 5 also omits the proposal's A.3 remote check (`verify_project`, 4400-4404). Exact words: in rule 5 replace "a sentence-final period blocks a match, which fails toward unattributed" with "a `.` counts as an end when the byte after it is not a letter, digit, `_` or `-`; any byte of 0x80 or above after the root blocks a match; blocks overlap by the root's length plus 7 bytes"; after "the replies carry it" add "if that project passes `verify_project`, as Claude's do"; replace S4 with "S4: a missing or unreadable file, or a cap, leaves a conversation unattributed; a second project named only in a spelling the rule misses gives the conversation to the first (accepted, a wrong report figure)". C2 adds: a root split across a block edge; `/x/cairné`; the period case.

B2. **Caps and opens are underspecified where they matter.** The plan does not say which counter the new walker and the search charge. If either charges `MAX_REFRESH_ENTRIES` or `MAX_SOURCE_FILES`, a large `brain/` raises `source_budget_exceeded` and fails the refresh for Claude and Codex too (2815-2816). "Opens files without following" is false on Windows (`_O_NOFOLLOW` is 0, 335), and no open checks middle folders (827). Exact words: add to rule 5's Bounds "Search entries and bytes charge only the per-conversation caps and a per-refresh cap of 50,000 entries; over it, conversations wait (`catching_up`); the log walker stops at 2,000 conversations the same way; nothing in Antigravity's reader raises `source_budget_exceeded`. Each opened file's `fstat` device and inode must equal the walk's `lstat`, or the search is incomplete." C3 adds a refresh with Claude and an over-cap `brain/` where Claude still counts.

**Non-blocking**

N1. `antigravity_unattributed` sits in the ledger's reasons, which every export copies (2394), so every project, Claude- and Codex-only ones too, prints INCOMPLETE from the first refresh (4 conversations with tokens name no folder). State it; the Maintainer chooses.
N2. Inferred events marked `proven` also feed the claim-to-artifact join (`_build_mappings`, 3116-3120); "no gate reads it" should say so. The export still tells inferred rows by tool and reason.
N3. W1's share check repeats the look's own rule, so it tests the build, not the attribution; add a hand-labelled sample by the Maintainer and a count of conversations over each cap.
N4. A hard link to `~/.gemini`'s credential file is a regular file and would be searched; only a yes/no leaves. Name it in S5.

Consent (7), what leaves (4: fixed reason strings, digests of random ids, cursor keys digested at 2822) and the label (5) hold.

**Verdict**: REVISE

**Coverage**: read the plan, the look and Addendum, the proposal's rule A and Security review, the privacy rules, `meter.py` 30-470, 790-860, 2300-2410, 2791-3000, 3089-3275, 3551, 4400-4420, `pulse.py` 37-60, 455-470. Not read: `_conversation_project` (unbuilt), `read_records` body, tests, the usual review. Ran no test; read no Antigravity file or `meter.json`. Over target: two blocking findings need exact words.
**Elapsed**: about 25 minutes
**Tokens**: unknown

## Plan review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-22

```
Reviewed commit: 149606373bc17f885fe7fe8e1a72e2f5a8f3adeb
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised (three blocking)
**Verdict**: REVISE

**Elapsed**: unknown. **Tokens**: unknown.

Every `meter.py` line number the plan cites is right (the edit lines 1977, 2394 and 3246 sit inside their functions), the twins are byte-identical (`cmp`), and the counts match the look and its Addendum. Wrong facts: INCOMPLETE "beside every row" (finding 4); "368 node ids" (366 in `test_meter.py`, 2 more in `test_git_read_routes.py`); "1,500 target" (the template says 1,000); "no other file runs" (finding 7). The roster and manifest claims hold by grep.

**Foundations**

1. **Should this happen as framed?** Yes. B is the smallest reading that gives a project figure, and the accepted cost-per-plan proposal ties a run's replies only "in the same project" (`dev/proposals/2026-11-22-claude-cost-per-plan.md`, Proposal item 3), which a project-less total cannot do.
2. **Best alternative.** Option A plus stage declarations avoids the trust change but needs that tie relaxed and gives no project figure "like Claude and Codex", which his words ask for; B stays (`dev/measurement/antigravity-look-2026-11-22.md`, "The choice").
3. **What would show it wrong.** W1 attributing far fewer than the look's 40 of 48 conversations (the caps are unmeasured starting values), or folder names that differ from `ANTIGRAVITY_TRAJECTORY_ID`, so no agent could declare the run.

**Findings**

1. **Blocking: C2 cannot pass its own test.** Its entry is "a synthetic refresh", but the walker and scan edits are in C3. Replace rows C2 and C3 with: "C2 | Wiring and attribution | C1 | `_enumerate_antigravity`, the `_scan_approved_sources` edits at 2813, 2910 to 2946 and 2951, `_conversation_project`, the constants, the two refresh tests" and "C3 | Labels and records | C2 | the two reasons and their test, both READMEs, changelog, names list, board rows, lock". This also splits an overloaded C3.
2. **Blocking: C1 leaves design open.** Synthetic lines carry no conversation. Add to C1: "For a stream the id is the second part of `lines.relative` and must satisfy `str(uuid.UUID(x)) == x`; `read_records` takes a keyword `conversation` for synthetic lines, and C1's tests pass it. A record whose `conversationId` or `conversation_id` differs gives no event and `conflicting_binding`; both names join `created_at` in the names list." Name the model key (`model`) or delete the branch (0 of 12,268 records name one; deleting is lighter).
3. **Blocking: C2 and C3 leave failure and budget design open.** Add: "A missing `brain/` or `logs/` gives no files, and an error inside one conversation skips it with `catching_up`; only a missing or linked root raises `Unavailable`, which ends the refresh for Claude and Codex too (2813). The walker returns `(files, entries)` as `_enumerate_jsonl` does and counts against `MAX_REFRESH_ENTRIES` and `MAX_SOURCE_FILES`. Search blocks overlap by the longest project path plus one byte, and one C2 case straddles a block edge. A conversation is searched only if `attribution_bytes + MAX_ATTRIBUTION_BYTES <= MAX_ATTRIBUTION_RUN_BYTES` and `total_bytes + MAX_ATTRIBUTION_BYTES <= MAX_RUN_READ_BYTES`; otherwise its files are skipped as at 2829 to 2834. The three attribution reasons are event reasons, not batch issues."
4. **Non-blocking: the INCOMPLETE cost is acceptable but misdescribed.** The pulse prints it once, on the report's header line (`pulse.py` 880 to 886), and `antigravity_unattributed` reaches every project's report because it rides the ledger's reasons (`meter.py` 2394). A benign reason is not printed (`pulse.py` 466 to 469), so the offered one-line change would hide the label, not fix it. End rule 6 with: "The pulse prints INCOMPLETE once per report while any Antigravity conversation is unattributed, so it no longer tells a cut-short refresh from this; accepted, since unattributed tokens may be any project's."
5. **Non-blocking: overpromise.** Add to Build summary: "Antigravity rows carry input and output only: no model, no cache counts, so the pulse shows weighted=unknown. They say how many tokens, not what they cost." His words do not name B; ask him once in chat before C3 closes the board's wait.
6. **Non-blocking: run identity.** Whether the folder name equals `ANTIGRAVITY_TRAJECTORY_ID` decides if the identity ever joins a declaration. A names-only check settles it: compare the 10 distinct `antigravity-<8 hex>` tags in `dev/intents.jsonl` with `sha256(folder name)[:8]` of the `brain/` folders (`_intent/identity.py` 51). Do it before C1 fixes the key; changing it later changes every event key.
7. **Non-blocking: controls and runs.** Decoys in `chunks/` and a non-UUID folder must carry different counts (an identical copy dedupes and hides a read, and an `os.open` spy "under the root" cannot see them); assert the exact set of opened paths. C2 lacks the byte-before cases (a letter before; `file://` before) and the entry and depth caps. Merge the two C3 tests into one refresh. Run `tests/test_meter_claude_usage.py` and `tests/test_meter_usage_free_records.py` (543 lines, sharing the merge code) with `test_meter.py`, once, at C3 only; the file took 2.7 s for 366 cases (`dev/measurement/certification-run-2026-11-12-per-file.csv`), so "about 1 minute" is loose. Add the neutrality and snippet gates for prose. Reuse `_usage_values` (3784) and `_codex_uuid` (3476).
8. **Non-blocking: length.** The 2,440-word body is half justified: a low-tier executor and a trust change want each limit stated, but the probe results appear twice (Scope and rule 3) and rule 6's rejected column is not needed to build; about 300 words could go, and findings 1 to 3 add about 200.

**Coverage**: read the plan, look and Addendum, Mac check, the cost-per-plan Proposal section, `meter.py` at every cited line plus `_enumerate_jsonl`, `_ApprovedLineStream`, `_scan_approved_sources`, `_new_ledger`, `_project_export`, `_merge_retained_event`, `_validate_event`, `pulse.py` 40 to 45, 311 to 380, 466 to 469 and 880 to 886, the stub test and mirror test, the manifest and roster (JSON load and grep), and the lock by grep. Plan text is the same at the later Security review commit `758e3d55` (35 lines added, none removed). Not read: the Security section, any Antigravity file, `~/.cairn/meter.json`; no test or collection run; Windows spellings, the lock's hashes and the folder-name question unchecked. Over the 300-word target because the Maintainer asked for line-by-line checks and three blocking findings carry exact words.
