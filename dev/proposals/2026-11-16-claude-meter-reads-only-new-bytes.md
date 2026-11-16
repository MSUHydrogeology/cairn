# The usage meter counts forward from a start point and reads only what is new

**Author**: Claude Opus 5.5 (`claude-opus-5-5`), Strategy
**Status**: awaiting-decision
**Review**: usual + Security Review
**Proposed tier**: standard — raised from light after review: the change now covers the ledger's retention, the refresh receipt and the pulse report as well as reading, so it needs a plan (the Maintainer sets the tier)
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-16
**In brief**: The meter would count usage from the day it is turned on, read each session log only from where it stopped, keep its ledger to a fixed size, and say plainly when a run is incomplete, so it works on projects of real size.

## Decision summary

The usage meter cannot complete a refresh on any project of real size, and fixing how much it reads is not enough. Measured on 2026-11-16: Claude Code's logs total 3.19 GiB in 2,591 files and Codex's 1.06 GiB in 361; each refresh re-reads every log from the start and refuses past 256 MiB. Its ledger also keeps every usage event for ever, up to 100,000 events (about 88,000 by its 64 MiB size limit), and the logs already hold about 170,000 distinct Claude replies carrying usage (383,000 lines, since Claude Code repeats one reply's usage on several lines) and 59,000 lines carrying Codex usage, not yet de-duplicated. So the meter would stop again within weeks even if it read only new bytes.

Proposed: (A) count forward from a start point instead of back-filling history; (B) read each log from its saved bookmark, counting only this run's bytes against the limit; (C) keep individual events only for a short window and fold older ones into daily totals; (D) report an incomplete run as `partial`, never as complete. The Maintainer chose the direction on 2026-11-16: "Count only new bytes, 256mb seems pretty arbitrary to me". The cost is a ledger format change and a plan.

## Context

Read in `tools/meter.py` at `d8392bb9` (its twin `templates/skills/_lib/meter.py` is byte-identical), with the two reviews below:

- **Reading.** Each log's full size counts against `MAX_TOTAL_SOURCE_BYTES` (256 MiB) before it is read; each log is streamed from byte 0 under `MAX_BATCH_BYTES` (64 MiB, also the reader's own ceiling at line 1230). Saved cursors are never used to skip bytes. A log that grows during the read ends the whole run as `source_changed`, and `bytes_read` includes a partly written last line (ordinary review, reproduced).
- **Parsing.** Codex lines depend on earlier lines in the same log (session header, turn contexts, fork markers). Read from the middle, they lose their owner and project, and the merge keeps that loss (ordinary review). Claude lines stand alone.
- **Retention.** `MAX_RETAINED_EVENTS` is 100,000 and `MAX_LEDGER_BYTES` 64 MiB; a run that would exceed either is discarded and saves no cursor. Event keys are derived from content, so reading a line twice cannot count it twice (Security Review).
- **Receipt.** The refresh receipt has three statuses (`ok`, `disabled`, `unavailable`) and coverage is always `unknown`. A skipped partly written log already adds a reason and still reports `ok` (Security Review, reproduced). `tools/gauge.py` accepts any reason label and does not show it.
- **Goodnight.** `tools/session.py session-end --handoff` refreshes the meter before its two prunes and skips both, exiting 5, unless the receipt is `ok` or `disabled`. Since the consent file was created on 2026-11-16 the receipt is `unavailable`, so the handoff prune now always stops.

No recorded rationale exists for 256 MiB or 64 MiB (the total arrived in `a5230774`, the per-log value in `166e5bc8`). A plain read-and-parse of 315 MiB of real logs ran at about 263 MiB/s on this machine; the meter does more work per line, so its rate is lower and not yet measured.

## Proposal

**A. Count forward from a start point.** When the meter first runs after this change, or when a project is first added, it records the end of each existing log as that log's starting bookmark and counts nothing before it. Only usage written after the start point is counted. Logs created later are read from their first line. Back-filling history is not offered in this change.

**B. Read only new bytes, safely.**
1. A Claude log resumes from its bookmark only if all four hold: the bookmark is not past the log's current size; the byte before it is a newline; a saved digest of the last complete line before it still matches; and the device and inode are unchanged. Otherwise it is read from its first line (or, for a log older than the start point, set to a new start bookmark), and a reason is recorded.
2. A Codex log is read from its first line each time it grows, because its lines need earlier context. A later plan may save the parser's state instead; this change does not.
3. Each run reads at most the size a log had when it was opened, so a log that grows during the read is not an error; the rest is read next time. The bookmark is the offset after the last complete line; a partly written last line is left for the next run.
4. Limits count bytes read in this run, including digest re-reads and Codex re-reads. Per log per run: 64 MiB (`MAX_BATCH_BYTES`, unchanged); a larger log is read in pieces at line boundaries. Per run in total: 1 GiB, provisionally; the implementer times a real refresh and lowers it if a run takes more than 60 seconds, recording the measured rate beside the constant.

**C. Keep the ledger to a fixed size.** Individual events are kept for 14 days, long enough to match copied Codex fork history (the existing `_verify_copied_forks` and `parent_cursors`). Older events are folded into daily totals per project, tool and model, which are what the pulse report shows. The plan must show that a fork copying history older than the window is still not counted twice, or keep those events longer.

**D. Say when a run is incomplete.** The receipt's statuses become a closed set of four: `ok`, `partial`, `disabled`, `unavailable`. `ok` only when every approved log was read to its current end with no skipped log; reaching a limit gives `partial` with reason `catching_up`; any unrecognized value counts as incomplete. The per-project summary and the pulse report print `incomplete` and the reason. Usage counted so far is kept.

**E. Goodnight.** `tools/session.py` is not changed: it treats anything but `ok` or `disabled` as unavailable and skips the prunes, which is safe. So the handoff prune runs again once the meter reports `ok`. Until this change lands, the Maintainer can set `"enabled": false` in `~/.cairn/meter.json` before running the handoff prune.

Counts, cursors and digests are saved together in one atomic replacement of the private ledger (as today), under a new ledger schema version; a ledger in the old version is kept as history and the new one starts from a start point. Digests, cursors and Codex state stay in the private ledger and never enter the per-project summary.

## Rationale

Counting forward makes each run's cost follow new use, and the fixed-size ledger keeps the meter working for months, not weeks. The Maintainer wants to start seeing reports; history before the start point is not needed for that.

## Alternatives considered

- **Back-fill all history in steps.** The original draft. It needs the retention change anyway, takes many runs, and Codex logs cannot be resumed without saved parser state.
- **Raise the limits only.** Each run still re-reads gigabytes, and the 100,000-event ceiling stays.
- **Trust device, inode and size, with no digest** (ordinary review's alternative). Cheaper, but a rewritten last line would be resumed past silently; the digest costs at most one line per log.

## Documentation / doctrine surface

`dev/measurement/README.md` (meter section): the start point, `partial`, the 14-day window and the goodnight workaround. One `CHANGELOG.md` entry. No doctrine, template or always-loaded file changes.

## Evidence / verification plan

### Tests required

Through the public `refresh` entry point on synthetic logs, in `bootstrap/tests/integration/test_meter.py`: a first run sets start bookmarks and counts nothing before them; a grown Claude log resumes and the total equals a full read of the new part; each of the four resume checks, failing, restarts; a log growing during the read ends `ok` or `partial`, never `source_changed`; a partly written last line is not counted until complete; a Codex log is re-read and keeps its owner and project; a run over the limit returns `partial`, never `ok`, and later runs finish; events past 14 days fold into daily totals with unchanged sums; a copied fork is not counted twice; the per-project summary and the pulse show `incomplete` and the reason; digests and cursors never appear in the summary. Rewrite `test_refresh_total_source_budget_is_all_or_unavailable`; cover the Windows reader and the twin-parity check. Then run the test files `python tools/test_tiers.py for` lists, and one real refresh on this machine, timed.

### Security preflight

- S1: inputs are the person's approved logs; unchanged.
- S2: new trust is the saved bookmark and digest in the private ledger. A forged bookmark can make the meter skip new lines (an undercount) but cannot widen what is read.
- S3: a failed resume check restarts or resets, never skips forward. The digest covers only the line before the bookmark; logs are assumed to be appended to, not edited in place. An in-place edit further back would go unnoticed, and because event keys come from content it cannot cause double counting.
- S4: `partial` and unrecognized statuses never print as complete.
- S5: same-user tampering with the private ledger stays outside the meter's model.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A run that stopped early reports `ok`; resumed and full reads of the same new lines give different totals; daily totals change when events are folded; a fork is counted twice; or a goodnight refresh takes more than a minute after the first run.

## Scope delta

Widened after review, with the author's reasons in the Response: retention (C), the receipt and pulse (D) and the start point (A) were added; back-filling history was dropped.

## Assurance path

**Assurance path**: standard. It changes how a shipped tool reads and keeps private data. The plan's Security Review checks B1, C and D first. The meter is not frozen in the gate manifest, so no re-anchor follows; `tools/session.py` is not edited.

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

## Response -- Claude Opus 5.5 (author) -- 2026-11-16

**Elapsed**: about 25 minutes. **Tokens**: unknown.

All findings are accepted. I checked the code the reviews cite and measured the real logs (line counts only; no content was printed). The operative text above is rewritten in place, and the scope widened, so the proposed tier rises to standard with a plan.

Ordinary review (REVISE):

1. **Accepted (blocking).** Codex logs are re-read from their first line when they grow (B2); only Claude logs resume.
2. **Accepted (blocking), and worse than the review could show.** Counted: about 383,000 lines carry Claude usage and 59,000 carry Codex usage, against a 100,000-event ceiling. Back-filling cannot fit, and even counting forward would reach the ceiling within weeks. Two changes answer it: the forward start point (A) and the 14-day window with daily totals (C).
3. **Accepted (blocking).** D defines `partial`, its reason, and what the summary and the pulse print. `tools/session.py` is deliberately not changed; it already skips the prunes on anything but `ok` or `disabled` (E).
4. **Accepted (blocking).** B3 reads only up to the size at open and sets the bookmark after the last complete line.
5. **Accepted (non-blocking).** S3 now states the append-only assumption and what the digest does not catch.
6. **Accepted (non-blocking).** The atomic ledger write, the schema version, the test to rewrite, the Windows reader and the twin check are named. The wrong sentence about `rebuild` is gone.

Security Review (REVISE):

1. **Accepted (blocking).** D: a closed set of four statuses; `ok` only when every log was read to its end; anything else is incomplete and printed as such.
2. **Accepted (blocking).** B1 lists the four resume checks; a failure restarts or resets with a reason.
3. **Accepted (blocking).** B4 counts digest and Codex re-reads in the limit and names the values: 64 MiB per log (the reader's own ceiling) and 1 GiB per run, provisional until a timed real run.
4. **Accepted (non-blocking).** Digests, cursors and Codex state stay in the private ledger; a test checks the summary.

Also found while checking: since the consent file exists, `session-end --handoff` stops before its prunes (E gives the workaround). Both reviewers' notes on `501f1c1e` and `fb09a793` found no defect.

**For the Maintainer.** (1) Count forward from a start point, with no back-filling of history? Default: yes. (2) Tier standard with a plan? Default: yes. (3) A 14-day event window? Default: yes, unless the plan shows forks need longer. Because the scope widened, a targeted second review of A and C before the Decision is allowed; I do not think it is needed, since the plan's reviews will examine the design in detail.

## Correction -- Claude Opus 5.5 (author) -- 2026-11-16

The Response's finding 2 counted log lines, not events. Claude Code writes one reply's usage on several lines; counting distinct message IDs gives 169,738 replies (383,361 lines; 3,765 usage lines carry no message ID). Codex's 59,452 lines are not yet separated into distinct events. The conclusion stands: the total exceeds the 100,000-event ceiling. The Decision summary now gives the corrected figure.
