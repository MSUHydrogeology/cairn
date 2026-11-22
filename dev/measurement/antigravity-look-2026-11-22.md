# Antigravity's saved files: a count-only look (2026-11-22, Mac)

This is the one look the [usage-counting proposal](../proposals/archive/2026-11-21-claude-usage-counting.md) (part D) asked for before anything is built for Antigravity. It follows the proposal's rule: counts, and field names from a fixed list; nothing copied. The Maintainer's word to run it: *"You have my permission for all items on this board"* (chat, 2026-11-22).

## Answer

**Antigravity's saved files hold token counts, with a time on every record, but no working folder.** So a reader can count the tokens, but it cannot tell from a record which project they belong to. The proposal's test for building a reader was "token counts and a working folder"; the second half is not met. A reader needs an attribution rule, which is the Maintainer's to choose (below). A reader must also remove duplicates: each token record is written about four times.

## What was measured

All of it on the Mac, in the folder Antigravity keeps for its saved work (9,330 files: 5,289 `.txt`, 912 `.json`, 806 `.jsonl`, 498 `.log`, 46 SQLite databases, the rest program or image files; program folders were skipped). One credential file beside it was not opened. The scripts printed only counts keyed by the fixed lists, so no value, path or text appears here.

| Question | Count |
|---|---|
| Records that hold `input_tokens` and `output_tokens` | 24,339, every one with a positive number in both |
| Of those, records that also carry a time field | 24,339 (all text) |
| Where the token fields sit | at the top of the record, in all 24,339 |
| Distinct token records, by conversation, time, input and output | **6,134** |
| Where they are written | 12,268 in `logs/*.jsonl` (6,134 distinct, each twice) and 12,071 in files one folder below `logs/chunks/` (6,128 distinct, all also in `logs/`) |
| Token records that name a model in the same record | 92 of 24,339 |
| Token records that name a `workspace` in the same record | 81 of 24,339 |
| Values of any `workspace` field in JSON | 105: 4 absolute paths, 101 not a path; none is this project |
| The one SQLite table with a `workspace` column | 73 rows: 66 empty, 7 text that is not a path; none is this project |
| Conversation folders under `brain/` | 48; 45 hold token records |
| Conversations whose saved files name this project's root | 40 (39 of them hold tokens) |
| Conversations that name another folder under `Code/` | 8; 5 name both this project and another |
| Conversations with tokens that name neither | 4 |
| Share of token-key occurrences in conversations that name this project | 19,836 of 24,535 (81%) |

Fixed lists used: token (`input_tokens`, `output_tokens`, `total_tokens`, `inputTokens`, `outputTokens`, `totalTokens`, `promptTokenCount`, `candidatesTokenCount`, `totalTokenCount`, `cachedContentTokenCount`, `thoughtsTokenCount`, `tokenCount`, `token_count`, `tokens_used`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `usage`, `usageMetadata`, `usage_metadata`); folder (`cwd`, `workspace`, `workspaceFolder`, `workspace_path`, `workspaceUri`, `projectPath`, `project_path`, `rootUri`, `workingDirectory`, `working_directory`); identity (`sessionId`, `session_id`, `conversationId`, `conversation_id`, `cascadeId`, `trajectoryId`, `requestId`, `request_id`, `messageId`, `message_id`); model (`model`, `modelName`, `model_name`); time (`timestamp`, `created_at`, `createdAt`, `ts`, `time`, `startTime`, `start_time`, `endTime`, `end_time`, `date`, `updatedAt`, `updated_at`). Only `input_tokens`, `output_tokens`, `model`, `modelName`, `conversationId`, `conversation_id`, `request_id` and `workspace` were found; the rest never appeared.

## What it means for a reader

- **Tokens exist, so Antigravity usage can be counted.** There is no cache-read or cache-write count and no named usage object, only two numbers per record.
- **Deduplicate, or the total is about four times too high.** A record's key for that is conversation, time, input and output. A genuine second reply with the same time and counts would be dropped; the look cannot tell whether that happens.
- **The record does not say which project it belongs to.** The only project signal found is in the conversation's saved files, which name project folders in 40 of 48 conversations. That is weaker than the Claude and Codex logs, where each record carries its own working folder; text in a file can name a folder for any reason.
- **The model is almost never in the same record** (92 of 24,339), so a weighted total, which needs the model, cannot be computed for most of it.

## The choice this leaves (the Maintainer's)

A. **Count Antigravity tokens as a machine-wide total shown on its own, tied to no project.** Simple, honest, needs no trust in file text. It does not give a cost per project.
B. **Attribute a conversation to a project when its saved files name that project's root and no other project's**; conversations naming several, or none, stay unattributed and are shown as such. Gives about 81% of the tokens to this project here, by inference. It changes what the meter trusts, so it takes a Security Review under the proposal's rule.
C. **Leave Antigravity out, with the reason shown**, as the proposal allowed if the test failed. The Maintainer's word of 2026-11-21 is that excluding it was a defect, so this needs his word.

Recommendation: A first, since it counts tokens without widening trust, and B as a second step only if he wants cost per project. Not decided; nothing is built.

## Not checked

The look did not decode the protobuf files (`conversation_summaries` and similar; field names are not stored in them), did not read any SQLite value except whether a `workspace` text is a path, and did not inspect `~/Library/Application Support/Antigravity` or its logs. It ran once, at one moment on one machine; the Antigravity version was not recorded. Whether the 4 conversations that name no folder are the Maintainer's other work was not looked into. No model name, price or weight was checked against these records.
