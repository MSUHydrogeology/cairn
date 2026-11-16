# The usage meter reads only what is new in each session log

**Author**: Claude Opus 5.5 (`claude-opus-5-5`), Strategy
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: light — one shipped tool and its twin change how much they read per run; no install, template or doctrine change (the Maintainer sets the tier)
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-16
**In brief**: The meter would read each session log from where it stopped last time and limit only the new bytes per run, so it works on projects of real size and catches up on old logs over several runs.

## Decision summary

The usage meter cannot complete a refresh on any project of real size. Each run re-reads every session log from the start and refuses once the logs together pass 256 MiB, or any one log passes 64 MiB. Measured on 2026-11-16: Claude Code's logs total 3.19 GiB in 2,591 files and Codex's 1.06 GiB in 361 files; 14 single logs exceed 64 MiB. So token capture, turned on that day, reports `source_budget_exceeded` every time.

Proposed: each log is read from its saved bookmark, and the limits count only the bytes read in this run. A run that reaches the limit stops cleanly at a line boundary, records how far it got, and reports that it is catching up; the next run continues. The Maintainer chose this on 2026-11-16: "Count only new bytes, 256mb seems pretty arbitrary to me". Cost: a check that a log's earlier bytes have not changed, and tests for resuming and catching up.

## Context

Read in `tools/meter.py` at commit `d8392bb9` (its twin `templates/skills/_lib/meter.py` is byte-identical):

- `_scan_approved_sources` adds each log's full size to `total_bytes` before reading it and refuses past `MAX_TOTAL_SOURCE_BYTES` (256 MiB). Each log is then streamed from byte 0 through `_iter_approved_lines`, whose per-log budget is `MAX_BATCH_BYTES` (64 MiB).
- Each log already gets a saved cursor (`offset`, `line`, size, times, device and inode), but nothing uses `offset` to skip bytes already read. A log that grew counts as "changed" and is read again in full.
- Other limits stay as they are: 1 MiB per line, 10,000 files, 100,000 directory entries and 100,000 normalized events per run.

How fast the logs grow is not measured directly. Logs touched in the last day hold 522 MiB (Claude) and 193 MiB (Codex), but that is their whole size, not the new bytes in them.

The 256 MiB and 64 MiB values have no recorded rationale in the Meter plan that I found. They bound one run's reading time and memory; the stream already holds at most one line in memory at a time.

## Proposal

1. **Resume from the bookmark.** For a log whose device, inode and size show it only grew, start reading at its saved `offset`, at a line boundary, and count lines from its saved `line`.
2. **Check the bytes before the bookmark.** Save a digest of the last complete line before the bookmark (at most `MAX_LINE`, 1 MiB). On resume, read that window again and compare. If it differs, or the log shrank, or its device or inode changed, treat it as a new log and read it from the start.
3. **Limit only new bytes.** The per-run limit counts bytes read in this run, including any restarted logs. The per-log 64 MiB limit applies to bytes read from that log in this run, so a log larger than that is read in pieces across runs.
4. **Catch up in steps.** At the limit, finish the current line, record cursors for everything read so far, and end with a new status, `partial` (reason `catching_up`), never `unavailable`. Usage counted so far is kept; the reported coverage says it is incomplete. The next run continues from the cursors.
5. **The values.** Keep a per-run limit, because it bounds how long one run takes at session end. Choose its value in the change from a measured read rate on this machine, aiming at under a minute per run, and record the rate and the reasoning beside the constant. The per-log limit becomes the same value, since it no longer guards whole-file memory.
6. **No double counting.** Events already in the ledger are not counted again. The ledger already keys each event (`event_key`); the change confirms that a resumed read and a restarted read give the same keys for the same lines.

The `refresh` and `rebuild` commands, the consent file, the per-project summary and the privacy rules do not change. `rebuild` still reads from the start, under the same per-run limit, so a rebuild also proceeds in steps.

## Rationale

Re-reading every log in full makes a refresh cost grow with all history, not with new use; no fixed limit fits that for long. Reading only new bytes makes a session-end refresh cost about one session's logs.

## Alternatives considered

- **Raise the limits.** Simplest, but each run still re-reads gigabytes, and the cost keeps growing.
- **Narrow the sources.** Measured: every project folder of real size already exceeds 256 MiB (Cairn's alone is 1.5 GiB).
- **Make the limit a consent-file setting.** Adds a privacy-file field for a performance choice. Not needed once runs read only new bytes.

## Documentation / doctrine surface

`dev/measurement/README.md` (the meter section): say that the first runs catch up in steps and what `partial` means. One `CHANGELOG.md` Fixed line. No doctrine, template or always-loaded file changes.

## Evidence / verification plan

### Tests required

Through the public `refresh` entry point, on synthetic logs in `bootstrap/tests/integration/test_meter.py`:

- A log that grows between two runs: the second run reads only the new bytes and the totals equal one full read.
- A log rewritten before its bookmark (same size, changed earlier line): it is read from the start, and nothing is double counted.
- A log that shrank, or was replaced (new inode): read from the start.
- Logs larger than the per-run limit: the first run ends `partial` with usage kept; later runs finish; the final totals equal one unlimited read.
- A run that stops mid-file resumes at a line boundary, never mid-line.

Then run the test files that name `tools/meter.py`, as `python tools/test_tiers.py for` lists them. A real refresh on this machine must complete in steps and then report counts.

### Security preflight

- S1: the input is the person's own approved session logs; unchanged.
- S2: the new trust is the saved cursor, which lives in the private ledger under `~/.cairn/meter/`. A forged cursor could skip bytes (undercount) but cannot widen what is read: reads stay inside approved roots, under the existing no-follow and identity checks.
- S3: the bytes-before-bookmark check makes a changed log restart rather than resume, so it fails toward reading more, never toward skipping.
- S4: `partial` reports incomplete coverage and never reads as zero use.
- S5: same-user tampering with the private ledger stays outside the meter's model, as today.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A resumed run counts different totals than a full read of the same logs; a log edited in place is resumed instead of restarted; or a session-end refresh still takes minutes after the first catch-up.

## Scope delta

N/A: opening proposal.

## Assurance path

**Assurance path**: standard. It changes how a shipped tool reads private data, so the Security Review checks items 2 and 4 in particular. The meter is not frozen in the gate manifest, so no re-anchor follows.

## Review -- Claude Sonnet 5.5 (ordinary Reviewer, Medium) -- 2026-11-16

```
Reviewed commit: e81f9c19ec00c535f738b9452bba4d3e74c18c81
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 6 minutes of clock time (13:21 to 13:27 EST, by `date`)
**Tokens**: unknown

The strongest case: a refresh whose cost follows new use, not all history, is the only kind that can work on logs this size, and the Maintainer chose it.

**Foundations**

1. **Should this happen as framed?** The direction is right; the specification is not yet safe, because resuming a Codex log is not a simple seek and the byte limits are not the only whole-history ceiling. -- `read_records` (Codex `owner` and `contexts` state), `MAX_RETAINED_EVENTS` line 101, `MAX_LEDGER_BYTES` line 107; findings 1-2
2. **Best alternative.** Trust (device, inode, size at least the offset) for append-only logs, resume Claude logs only, and keep `rebuild` as the repair for an in-place edit; no digest, no new cursor field. Doing nothing leaves the meter `unavailable` for good. -- `_CURSOR_FIELDS` line 2089 is a closed set; finding 5
3. **What would show it wrong.** A log edited at the same length on its first of three lines and then grown: the draft's own test expects a restart, but its digest sees only the last line. -- item 2 against the "rewritten before its bookmark" test; finding 5

1. **Blocking.** Codex records depend on earlier lines (session header, turn contexts, fork markers). Read from the middle, they are stored with unknown owner and project, and `_merge_retained_event` makes that mark permanent, so "totals equal one full read" fails for Codex. Close with a test (context before the bookmark, new usage after it) that matches a full read, or restrict resuming to Claude logs. -- `tools/meter.py` lines 5553-5800 and 2666-2750
2. **Blocking.** Catching up can stall on limits the draft keeps: 100,000 retained events and a 64 MiB ledger. One synthetic Claude event serializes to 761 bytes, so the ledger holds about 88,000 events; going over discards the run and saves no cursor. I did not count events in the real logs. Close with that count against 88,000, or a plan for the ceilings. -- `_merge_events` line 2762; probe in /private/tmp
3. **Blocking.** `partial` has no carrier. The refresh receipt is closed (`ok`, `disabled`, `unavailable`; coverage always `unknown`); `session.py` and its twin accept only `ok` or `disabled`, so a partial run would skip both goodnight prunes and exit 5; `gauge.py` prints `coverage=unknown` without reasons. Name the receipt, exit code, aggregate reason and pulse line, widen scope to those files, and test that a partial total never prints like a complete one. -- `_closed_refresh_receipt`, `_meter_refresh_receipt`, `gauge.py` line 1004
4. **Blocking.** Two edges are left open, and both reproduce. A log that grows during the read ends the whole refresh as `source_changed`, and other sessions are writing logs now. A torn last line is included in `bytes_read` (27 of 27 bytes for a 16-byte line plus an 11-byte fragment), so the cursor must be the offset after the last newline. State both rules and test them. -- lines 1280, 1326-1331, 3382
5. **Non-blocking.** The digest covers only the last complete line, so S3 ("never toward skipping") overstates. Either state the append-only assumption and drop the digest, or hash head and tail.
6. **Non-blocking.** Say that counts and cursors are saved in one atomic ledger replace, so a crash cannot split them. Give the cursor field a schema bump or optional field; this machine has only `ledger.lock`, so today's runs left nothing to migrate. `rebuild` runs the same code as `refresh` (`dev/measurement/README.md` lines 91-92), so "rebuild reads from the start, in steps" describes nothing. Name the test to rewrite (`test_refresh_total_source_budget_is_all_or_unavailable`), the Windows reader, and the twin-parity test. The per-run number may stay with the implementer if it must stay below finding 2's ceiling and advance at least one line.

**Coverage:** Read the committed draft, `meter.py` (reader, scan, merge, ledger, receipt), `session.py`, `gauge.py`, the Meter plan (no rationale for 256/64 MiB found; the 256 MiB total arrived in `a5230774`, the 64 MiB per-log in `166e5bc8`) and the relevant tests. Not covered: real logs (not opened), Windows, a full test run. Read the summaries and diffs of `501f1c1e` and `fb09a793`; they touch only SSH-remote normalization and do not contradict the draft. Security Review is separate. No shipped prose changes (the shipped README has no meter section), so no audience line. About 560 words: seven rules interact.

## Security Review -- Claude Opus (Security Reviewer, High) -- 2026-11-16

```
Reviewed commit: dc68e2efd270243babc35d4776a1db32a0cacb74
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: about 3 minutes of clock time (13:28 to 13:31 EST, by `date`)
**Tokens**: unknown

Obligation: can resuming from a saved cursor report a wrong or incomplete total as if complete, or expose log content, and what must fail closed?

The strongest case: event keys are content-derived (`_digest(tool, session, response, ...)`, lines 5578, 5711), so a bad cursor can skip lines but cannot double count.

**Foundations**

1. **Should this happen as framed?** Yes, once a partial run can never print as complete. -- `_closed_refresh_receipt` line 6117; probe below
2. **Best alternative.** None safer; a last-line digest is enough for logs a harness only appends to. -- event keys, lines 5578 and 5711
3. **What would show it wrong.** A catching-up run whose receipt says `ok`. -- the `partial_tail` path, lines 3376-3381

1. **Blocking.** The fault is a silent undercount. Today a skipped file (`partial_tail`) adds a ledger reason and the run still returns `written`, which the receipt prints as `ok` (probe in /private/tmp). `gauge.py` accepts any reason label (`_PULSE_LABEL`, line 221) and prints `coverage=unknown` either way. If catching up copies that path, every published total looks complete. Requirements: the receipt statuses form a closed set (`ok`, `partial`, `disabled`, `unavailable`). `ok` only when every approved log was read to its end. Any other value counts as incomplete; the receipt already maps unknown values to `unavailable`. The gauge and the project export state `incomplete` when the reason is `catching_up`. `session.py` may prune after `partial` only if claim capture finished. Close with a test that a catching-up run never yields `ok`.
2. **Blocking.** Resume only when four checks pass: the cursor is no later than the file's size; the byte before it is a newline; the window digest matches; and device and inode are unchanged. Any failure restarts from byte 0 and records a reason. Bound new cursor fields like today's (closed set, `_counter`; window at most `MAX_LINE` + 1). Path or control-character values are not a threat (`file_key` is hex; the alias passes `_safe_alias`).
3. **Blocking.** Count digest re-reads in the per-run byte limit. Up to 1 MiB per grown log is otherwise unbudgeted. Name the value; it must stay at or below `MAX_BATCH_BYTES` unless line 1230 changes.
4. **Non-blocking.** Keep digests, cursors and any Codex resume state in the private ledger, out of `_project_export` (it copies only aggregates and reasons today). Add a test for that.

**Coverage:** Read the draft, the ordinary review (not repeated), and in `meter.py` the scan, cursor validation, event keys, export and receipt; also `session.py` lines 1883-1912 and the `gauge.py` checks. Probe: an internal `partial` status becomes `unavailable/unavailable`. Not covered: real logs, Windows, tests. `501f1c1e`/`fb09a793`: no defect noticed. A Windows drive-letter remote now enters the SSH branch, but both sides normalize alike. About 400 words: four requirements.
