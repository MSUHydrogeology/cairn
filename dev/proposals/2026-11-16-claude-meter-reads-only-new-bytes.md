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
