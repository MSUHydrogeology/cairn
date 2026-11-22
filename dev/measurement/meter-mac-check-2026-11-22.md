# The simple meter on the Mac, checked against a real log (2026-11-22)

Job 6 of the Mac session (board, "Waiting on you"): repeat on the Mac the check Strategy made on the Windows Server machine, and answer the three Codex questions. The Maintainer's word: *"You have my permission for all items on this board"* (chat, 2026-11-22).

## Answer

**Met for Claude.** Between two refreshes the meter recorded 12 replies for this project, and an independent count of the same bytes found 12. All four token kinds are equal. Every text value in the project export is a time, a number or a short plain label. The Codex model names mostly match the table, and no Codex record carried a nonzero cache-write count.

## The Claude check

On a clean start (below), at 17:17:59Z the first refresh answered `ok` and counted nothing, as designed. At 17:18:49Z the second answered `ok`. The independent counter (a script written for this check; it takes each log file's offset from the saved cursors before and after, reads only the bytes between, keeps one record per message id and request id, and counts only records whose working folder is inside this project) found:

| | Meter | Independent |
|---|---|---|
| Replies | 12 | 12 |
| Fresh input | 24 | 24 |
| Output | 12,660 | 12,660 |
| Cache read | 5,239,815 | 5,239,815 |
| Cache write | 17,622 | 17,622 |

The bytes between were 185,124 in 2 files (94 lines, none unparseable). The meter filed all 12 under one model, `claude-sonnet-5-5`, with its provenance `usage_record`; that model is a row of the table, so the row carries weighted totals (705,570 weighted tokens in total).

## What it wrote

Project export after the second refresh: 17 text values, all of them a time, a number written as text, or a short plain label. The private ledger (`~/.cairn/meter/ledger.json`, 2.4 MB) holds mostly digests, times and labels; 251 values are none of those: 249 long strings under `targets`, one remote address and one 127-character `profile` text. It is private by design and I did not look further. No lock file was left behind, and the tracked tree stayed clean (the export is ignored by Git).

## The clean start

The first refresh answered `meter unavailable: ledger_old_schema`: the ledger on this machine was written by the old meter on 2026-11-19. The meter's README says to move it aside. I renamed it to `~/.cairn/meter/ledger.json.old-schema-2026-11-22` in the same folder and kept a second copy in scratch. The Maintainer's old totals are still there; the new meter starts again from zero, as the accepted usage-counting plan says.

## The Codex questions

Counted on the 8 most recent Codex logs (144,949 lines, 19,280 usage events):

- **Model names against the table.** The log names `gpt-6.1-terra` (84 turn contexts), `gpt-6.1-sol` (74), `gpt-6.2-sol` (6) and `codex-auto-review` (34). The first three are rows of the table; `codex-auto-review` is not, so its replies get no weighted total unless the table or the plan's choice (weighting by the turn's selected model, put to the Maintainer in plan J and unanswered) says otherwise.
- **Cache-write counts.** Every usage record has a `cache_write_input_tokens` field, and its value was zero in all 38,560. The reader's refusal of a nonzero count did not fire.
- **A weighted total for Codex work here.** Not shown by a refresh: no Codex record fell in the 50-second stretch, so the export held no Codex row. The names above say which Codex replies would be weighted.

## Not checked

One short stretch (50 seconds, 12 replies, 2 files) on one project. I did not check whether sub-agent transcripts or their summaries were among the new bytes, so the tie of a summary to its transcript is not shown. Not run: the end-of-session report (`refresh --report`), a long stretch, the other two projects in the consent file, Antigravity. The meter's counts were compared only with this script, written by the same session that ran the meter.
