# Plan: Defect arc H, the meter reads a real Claude log folder

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: The usage meter will read a real Claude log folder on Windows (sub-folders, logs with a second name) and will keep the date of Claude replies that the logs record in several pieces.

## Build summary

After plan G a real refresh on the Windows Server machine still answers `unavailable`. Measured on real Claude logs (counts only): the folder walk takes a sub-folder for a change and then fails a lookup on it; 16 of 132 logs have a second name made by the Claude desktop app; and on every platform 4,729 of 5,907 replies lose their date, because a reply is written as several records with different times. This plan fixes all four in `dev/tools/meter.py`.

## Source proposal

The accepted defect arc takes in defects found since.

## Scope

All in `dev/tools/meter.py`: `_enumerate_windows_jsonl`, `_WindowsApprovedLineStream.__iter__`, and the merge loop of `read_records`.

**(a) Sizes.** The size comparison applies to files only; identity and directory flag stay for every entry:

```python
or (not directory and info["size"] != row["size"])
```

**(b) First readings.** When a sub-folder's handle is added, record its reading so `verify` can look it up: `snapshots[child] = info` beside `all_handles.append(child)`.

**(c) Two names.** The walk accepts a file with `info["links"] != 1` unless it already met the same `info["identity"]` (a `seen` set), which raises `Unavailable("source_read_unavailable")` as today. The reader's `before["links"] != 1` test in `_WindowsApprovedLineStream.__iter__` is removed; its directory and volume tests stay. A refused file cannot reach the reader: the walk raises, so the refresh stops before any read, and `_check_stream_identity` refuses any stream whose volume and file id differ from the walk's record.

*For Security Review.* The old refusal guarded against one file read twice under two names. Kept: one file is never read twice in one walk; a second name outside the folder gives a reader no content the log does not already hold; the owner and access-list tests are untouched. The `hardlink` case (both names inside the folder) is still refused.

**(d) Reply times.** In the merge loop of `read_records`, when `tool == "claude"` and a later record of one event key has a different time, keep the earliest, leave the time known, add no `ambiguous_time`. Only while one log file is read; copies in two files (`_merge_event_batches`) keep today's rule; Codex is unchanged. Limit: a reply whose records fall in two refreshes meets `_merge_retained_event`, which still marks differing times `ambiguous_time`, so it loses its time. Not widened here.

**Reuse.** Searched `tests/integration/test_meter.py` for `hardlink`, `ambiguous_time`, `claude()`: T1 and T2 reuse the native fixture; the one time test is Codex and stays.

**Doctrine surface.** `dev/measurement/README.md` only. Not here: the `F:` drive access rights.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Tests first (fail), then (a) to (d), shipped copy, README, changelog | one code review | fixed meter, three tests |

## Acceptance criteria

- **T1 (Windows, native).** A log folder with a sub-folder holding a log and enough long-named entries that `os.stat(<sub-folder>).st_size > 0` (asserted). A real refresh answers `ok` and counts the nested log.
- **T2 (Windows, native).** A log with a second name outside the log folder (`os.link`). A real refresh answers `ok` and counts the log once.
- **T3 (every platform).** One Claude reply in three records, one usage, three times (`claude()` helper): one event, time known and the earliest, no `ambiguous_time`.
- The existing `hardlink` case passes, unedited.
- **Fixture defect, found now.** `_native_meter_setup` copies `meter.py` and `git_read.py` but not `pulse.py`, which `meter.py` loads at import (`_load_shared_pulse`), so every native case fails with `pulse-module-unavailable`. The build copies `dev/tools/pulse.py` there too, with its byte check. A defect fix, not new scope.

Also: `cp dev/tools/meter.py templates/skills/_lib/meter.py`, then `cmp` prints nothing; Cairn's lock by `install/scaffold.py upgrade --target . --finalize <paths>`, alone in its commit; `Fixed` lines under `## Unreleased` in `CHANGELOG.md`; the test file's gate-manifest hash is the Maintainer's signing line.

`dev/measurement/README.md`, after "the project's remote checks out.", add: "On Windows a log may have a second name (the Claude desktop app keeps one per background sub-agent); the Meter reads it once. A Claude reply logged in several pieces is dated by its earliest piece, unless the pieces fall in two refreshes."

## Verification

Write T1 to T3 first and run them once (they fail); change the code; run them once with `hardlink` (they pass), on Windows with `C:\ProgramData\Anaconda3\python.exe -m pytest tests/integration/test_meter.py -q -k "test_windows_native_meter_source_metadata_mutations and hardlink"` plus the T1 to T3 node ids. Nothing else is run; no stash.

**Measured now.** The `hardlink` case, run once here, failed with `pulse-module-unavailable` (the fixture defect). T1 and T2 run here after the fix.

**Strategy's checks, not the build's.** After the merge, a real refresh on the Windows Server machine; at the v0.8.1 cut, the Mac check against a real log.

## Plan review -- Reviewer (usual) -- 2026-11-21

Reviewed commit: 2e6c42274599f6d6cb5c555e3f4485d9a15adfe0

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Verdict**: REVISE. Changes (a), (b) and (c) are sound and small; (d) and the tests are not yet specified for a low-tier builder, and one gated record is missed.

**Foundations**

1. **Should this happen as framed?** Yes: the walk's directory size test and missing snapshot, the reader's link test and the merge loop's `_merge_normalized_event` call each match a refusal named in the plan -- `dev/tools/meter.py` lines 2205-2217, 1779, 7305.
2. **Best alternative.** None simpler for (a) to (c). T1 and T2 can be one native test (each fault alone refuses the whole refresh), saving a native run and a manifest row -- `tests/integration/test_meter.py` `_native_meter_setup`.
3. **What would show it wrong.** A real refresh on the Windows machine still answering `unavailable`, or T3 showing `ambiguous_time`; forward test is T3 plus Strategy's real refresh -- plan "Strategy's checks".

**Findings**

1. **Blocking: (d) is words only and "earliest" can be wrong.** Observed times are ISO text with offsets (`_timestamp`), so text order is not time order. Replace the (d) rule with this code, placed around the `_merge_normalized_event(merged[key], event)` call at the end of the loop:

```python
earlier = None
if tool == "claude":
    first, second = merged[key]["observed_at"], event["observed_at"]
    if first is not None and second is not None and first != second:
        earlier = min(first, second, key=datetime.fromisoformat)
_merge_normalized_event(merged[key], event)
if earlier is not None:
    merged[key]["observed_at"] = earlier
    merged[key]["time_coverage"] = "known"
    merged[key]["reasons"] = sorted(set(merged[key]["reasons"]) - {"ambiguous_time"})
```
An unknown time against a known one still loses the time, as today.

2. **Blocking: T1 and T2 have no recipe.** The first refresh only sets bookmarks and counts nothing. Say: run `_native_meter_successful_refresh`; then create the nested log (T1) or `os.link` the log outside the folder and call `_native_meter_append_valid_update` (T2); refresh once; `_native_meter_receipt(..., "ok", "none")`; assert one new event key, as `_native_meter_assert_update`. For T1 use 20 file names of 200 characters in the sub-folder and assert `os.stat(sub).st_size > 0`.

3. **Blocking: a gated record is missed.** New Windows-only tests are listed in `tests/security_manifest.py` (`NATIVE_ONLY_NODE_IDS`, bound to `NATIVE_ONLY_POLICY_ID`, read by `release/check_release_test_members.py`). Add the new node ids; leave the policy-id line as the Maintainer's signing line, with the gate-manifest hash. I did not run it.

4. Non-blocking: give (c) as code: `seen = set()` before the loop; replace the `links != 1` test with `if info["links"] != 1 and info["identity"] in seen: raise Unavailable("source_read_unavailable")` then `seen.add(info["identity"])`.
5. Non-blocking: say the Mac and Linux walk has no link or size test (`_enumerate_jsonl`), so only (d) reaches it.
6. Non-blocking: T3 should use equal usage in the three records; unequal usage is a separate conflict I did not check against real logs.
7. Non-blocking: tell the build not to attempt Strategy's real-machine checks.

**Not covered**: Security Review questions; real logs (privacy rule); the `F:` drive refusal; every other `links` test, which I read and found none on a log's path; I ran no test.

Elapsed time: unknown. Tokens: unknown.
