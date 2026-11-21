# Plan: Defect arc H, the meter reads a real Claude log folder

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-21
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: The usage meter will read a real Claude log folder on Windows (sub-folders, logs with a second name) and will keep the date of Claude replies that the logs record in several pieces.

## Build summary

After plan G a real refresh on the Windows Server machine still answers `unavailable`. Measured on real Claude logs (counts only): the folder walk takes a sub-folder for a change and then fails a lookup on it; 16 of 132 logs have a second name made by the Claude desktop app; and on every platform 4,729 of 5,907 replies lose their date, because a reply is written as several records with different times. This plan fixes all four in `dev/tools/meter.py`.

## Source proposal

The accepted defect arc takes in defects found since.

## Scope

All in `dev/tools/meter.py`: `_enumerate_windows_jsonl`, `_WindowsApprovedLineStream.__iter__`, and the merge loop of `read_records`. The Mac and Linux walk (`_enumerate_jsonl`) has no size or link test on a log, so only (d) reaches those platforms.

**(a) Sizes.** The size comparison applies to files only; identity and directory flag stay for every entry:

```python
or (not directory and info["size"] != row["size"])
```

**(b) First readings.** When a sub-folder's handle is added, record its reading so `verify` can look it up: `snapshots[child] = info` beside `all_handles.append(child)`. A folder that changes during the walk or the reads still refuses the refresh: `verify` compares its write time and ignores only the access time, which the walk's own reading changes. One cost: a log created in a sub-folder while a refresh runs now refuses that refresh, as one created in the log folder itself already did.

**(c) Two names.** `seen = set()` before the loop. In the file branch, the link test becomes:

```python
if info["links"] != 1:
    if info["identity"] in seen:
        raise Unavailable("source_read_unavailable")
    api.check_acl(child, user_sid, "profile")
seen.add(info["identity"])
```

So a file with a second name is read once, and only if it also passes the stricter `profile` access test, which refuses any other account's right to write it. The reader's `before["links"] != 1` test in `_WindowsApprovedLineStream.__iter__` is removed; its directory and volume tests stay. A refused file cannot reach the reader: the walk raises, so the refresh stops before any read. What still ties the file that is read to the file the walk accepted: `_check_stream_identity` (volume and file id, at open and at close), the reader's own `ancestor` access test, and the walk's `verify` after all reads.

*For Security Review.* The old refusal did two things. It kept one file from being read twice under two names: kept, by `seen`. And it was the only thing that stopped another account from planting, inside the log folder, a name for a file the user owns but that account can write: kept, by the `profile` test. A second name outside the folder gives a reader no content the log does not already hold. The owner and access-list tests on every file are untouched. The `hardlink` case (both names inside the folder) is still refused. A second name in another approved folder is read twice, and `_merge_event_batches` keeps one event for each key. Measured on the Windows Server machine with the meter's own `check_acl`, reading no file's data: all 16 logs with two names, and all 120 with one, pass the `profile` test.

**(d) Reply times.** In the merge loop of `read_records`, around the call `_merge_normalized_event(merged[key], event)`:

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

Times are compared as instants, not as text. An unknown time against a known one still loses the time, as today. Only while one log file is read; copies in two files (`_merge_event_batches`) keep today's rule; Codex is unchanged. Limit: a reply whose records fall in two refreshes meets `_merge_retained_event`, which still marks differing times `ambiguous_time`, so it loses its time. Not widened here. Nobody who cannot already write the log can use the rule to move usage to another day: only records in the one file read are compared.

**Reuse: no new test.** Both tests below are existing tests, changed. So no Windows-only test is added, and the list of such tests in `tests/security_manifest.py`, its count and its fingerprint do not change.

**Doctrine surface.** `dev/measurement/README.md` only. Not here: the `F:` drive access rights.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Fixture fix and the two changed tests first (they fail), then (a) to (d), shipped copy, README, changelog | one code review | fixed meter, two changed tests |

## Acceptance criteria

- **The native test (Windows only).** `test_windows_native_claude_resume_and_identity_on_a_spaced_root` in `tests/integration/test_meter.py` gains a last stage, after its `resume_failed_file_replaced` assertions, that gives its log folder the shape of a real one:

```python
    nested = setup["source"] / "session-alpha" / "subagents"
    nested.mkdir(parents=True)
    for index in range(12):
        (nested / (f"{index:02d}-" + "n" * 40 + ".meta.json")).write_bytes(b"{}")
    assert os.stat(nested).st_size > 0
    (nested / "agent-nested.jsonl").write_bytes(assistant("native-nested-first"))
    os.link(source, native_windows_root / "task-output-second-name")
    with source.open("ab") as handle:
        handle.write(assistant("native-crlf-linked"))
    before = {event["event_key"] for event in json.loads(ledger_path.read_bytes())["events"]}
    receipt, _out, _err = _native_meter_finish(_native_meter_start(setup))
    _native_meter_receipt(receipt, "ok", "none")
    after = [event["event_key"] for event in json.loads(ledger_path.read_bytes())["events"]]
    assert len(after) == len(set(after)) == len(before) + 2
```

  The sub-folder reports a size that is not zero (asserted, so the test fails if it stops exercising the point), the nested log is counted, and the log with a second name outside the folder is read once. Before the change this last refresh answers `unavailable`. If the folder's size is zero on the test machine, use more or longer names; do not drop the assertion.
- **The time test (every platform).** `test_same_message_twice_in_one_session_is_one_proven_event` in `tests/test_meter_claude_usage.py` reads three copies of one reply with one usage and three times, the earliest second in order. It keeps its three assertions and adds three: `time_coverage` is `known`, `observed_at` is the earliest time, and `ambiguous_time` is not among the reasons.
- The existing `hardlink` case passes, unedited.
- **Fixture defect, found while this plan was written.** `_native_meter_setup` copies `meter.py` and `git_read.py` but not `pulse.py`, which `meter.py` loads at import (`_load_shared_pulse`), so every native case fails with `pulse-module-unavailable`. The build copies `dev/tools/pulse.py` there too, with its byte check. A defect fix, not new scope.

Also: `cp dev/tools/meter.py templates/skills/_lib/meter.py`, then `cmp` prints nothing; Cairn's lock by `install/scaffold.py upgrade --target . --finalize dev/tools/meter.py dev/measurement/README.md`, alone in its commit; `Fixed` lines under `## Unreleased` in `CHANGELOG.md`; the gate-manifest hash of `tests/integration/test_meter.py` is one line at the Maintainer's signing, already owed from the usage-counting plan and plan G.

`dev/measurement/README.md`, after "the project's remote checks out.", add: "On Windows a log may have a second name (the Claude desktop app keeps one for each background sub-agent); the Meter reads it once, and only when no other account may write it. A Claude reply logged in several pieces is dated by its earliest piece, unless the pieces fall in two refreshes."

## Verification

Put the fixture fix in and change the two tests first, and run them once (they fail for their own reasons); change the code; run them once more with the `hardlink` case (they pass), on Windows:

`C:\ProgramData\Anaconda3\python.exe -m pytest tests/integration/test_meter.py tests/test_meter_claude_usage.py -q -k "test_windows_native_claude_resume_and_identity_on_a_spaced_root or (test_windows_native_meter_source_metadata_mutations and hardlink) or test_same_message_twice_in_one_session_is_one_proven_event"`

Nothing else is run; no stash.

**Measured when the plan was written.** The `hardlink` case, run once on the Windows Server machine, failed with `pulse-module-unavailable` (the fixture defect). Whether the native tests run on that machine once the fixture copies `pulse.py` is not yet known. If they cannot, the build stops and reports, and the native test runs at certification on the Windows machine.

**Strategy's checks, not the build's.** After the merge, a real refresh on the Windows Server machine gets past the walk and the reader. At the v0.8.1 cut, the Mac check against a real log. The build agent must not attempt either, and must not run the meter on real data.

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

## Plan review -- Security Review -- 2026-11-21

Reviewed commit: 085e30d1f063b9f03cd559a5306385aa3c6473b6

**Obligation**: Internal Security Review
**Tier**: Internal
**Findings**: raised

**Verdict**: REVISE. (a), (b) and (d) keep their protection; (c) opens one path the plan's security note misses. I agree with the usual review's findings 1 to 7; its (d) code governs, and is safe for Claude because a merged Claude event with a known time never already holds `ambiguous_time`. Either form of T1 and T2 (one test or two) serves.

**Foundations**

1. **Should this happen as framed?** Yes, with one added check: the old two-name refusal is the only thing that stops a planted name -- `dev/tools/meter.py` lines 2209, 2216.
2. **Best alternative.** Keep two names refused unless the file also passes the stricter `profile` access test; one line, no new test -- `check_acl`, lines 647-675.
3. **What would show it wrong.** Strategy's real refresh refusing the desktop app's second-name logs on the access test -- plan "Strategy's checks".

**Findings**

1. **Blocking: a planted second name.** The `ancestor` access test lets another account add files to a folder and write a file's data (mask at line 656 omits 0x2, 0x4, 0x100). Today such an account cannot plant a file the meter accepts: its own new file fails the owner test, and moving one in needs DELETE, which fails too. A hard link needs neither: it can put, inside the log folder, a name for a file owned by the user that the other account can write, and inject usage. In (c), after "unless it already met the same `info["identity"]`", add: "A file with a second name must also pass `api.check_acl(child, user_sid, "profile")`, which refuses any other account's write access." The `hardlink` case and T2 show it accepts the normal case.
2. Non-blocking: name what still ties the read to the walk: `_check_stream_identity` (volume and file id at open and close, line 4378), the reader's `ancestor` test, and `root_snapshot.verify()` after all reads (line 4423).
3. Non-blocking: (a) and (b) lose nothing. A folder change during the walk or the reads changes its write time, which `verify` compares; only `accessed`, which the walk's own reading changes, is ignored (line 1678). With (b), a log created in a sub-folder during a refresh now refuses it, as the root already did: an availability cost for Strategy's real refresh to watch.
4. Non-blocking: a second name in another approved folder is read twice; `_merge_event_batches` keeps one event per key (line 4544). (d) cannot move usage between days for anyone who cannot write the log: only records in the one file read are compared.

**Not covered**: real logs and their access lists (privacy rule), so I did not confirm real second-name logs pass `profile`; the `F:` drive refusal; I ran no test.

Elapsed time: unknown. Tokens: unknown.

## Plan response -- Claude Fable 5.2 (Strategy, for the author) -- 2026-11-21

Both reviews are folded once, in place. Status is now `ready-to-implement`.

Usual review:
1. Finding 1 ((d) in words only; text order is not time order): taken, with its code.
2. Finding 2 (the native tests have no recipe): taken, as exact code. Its question, one new native test or two: neither. The recipe is a last stage of the existing native Claude test, so no test is added.
3. Finding 3 (a new Windows-only test must join the list in `tests/security_manifest.py`): settled by adding none. A new row would also change that list's count and fingerprint, and the line that `tests/test_security_check.py` quotes from it: three frozen files for one test.
4. Non-blocking 4 to 7: taken ((c) as code; the Mac and Linux walk; equal usage in the time test; the build must not attempt Strategy's checks).

Security Review:
1. Finding 1 (a planted second name): taken, in its words. A file with a second name must also pass the `profile` access test. Its question, whether real logs pass that test: measured, all 16 logs with two names on the Windows Server machine pass it, with the meter's own `check_acl` and no file's data read.
2. Non-blocking 2 to 4: taken into (b), (c) and (d).

Changed in this fold beyond the findings, for the code review to judge: both tests are existing tests, changed, where the plan first named three new ones. The time test becomes `test_same_message_twice_in_one_session_is_one_proven_event`, whose two copies carried one time; that is why the usage-counting plan's tests did not see the fault.

Not run for this response: any test.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation closeout -- Claude Sonnet 5.5 (Implementation) -- 2026-11-21

**Commits** (branch `arc-h-impl`): `d0e4d9d7` status to implementing; `82df2b85` code, shipped copy, the two changed tests, README, changelog; `fb400b49` Cairn's lock (`verify_integrity` reports OK).

**As built.** (a) the size test applies to files only. (b) `snapshots[child] = info` when a sub-folder's handle is added. (c) `seen` set; a file with a second name is refused if already met, else must pass `check_acl(..., "profile")`; the reader's link-count test is removed. (d) the plan's code in the `read_records` merge loop, for Claude only. The fixture now copies `pulse.py` with its byte check. Both changed tests are as the plan gives them.

**Difference from the plan.** In (d) the time key is `lambda text: datetime.fromisoformat(text.replace("Z", "+00:00"))`, because plain `fromisoformat` reads `Z` only from Python 3.11, and the meter elsewhere strips it. In the time test the earliest-time assertion compares with the time a single record reads as (`read([rec()])`), since the stored form is `+00:00`, not `Z`.

**Command, before the code change** (the plan's one command): native Claude test failed, `hardlink` failed, time test failed on its new assertion (`unknown` not `known`). Both native cases failed at their first ordinary refresh (`_native_meter_successful_refresh`), before any of this plan's conditions: the receipt was `unavailable` with reason `unavailable`. This is this machine (probably the project folder's access rights on `F:`, the fifth finding), not the change. Two diagnostic reruns of `hardlink` alone, with traceback and locals, gave that location and reason.
**After:** time test passed (one further run of that test alone, after I corrected its expected time form). Both native cases failed at the same first refresh. So (a) to (c) are not exercised by any test here; they stay unproven until a Windows run where the fixture's first refresh answers `ok`.

**Not run.** Any other test; the real machines (Strategy's checks); the native tests to completion; the gate-manifest hash (the Maintainer's signing line).
Home: Strategy's checks after merge, and certification on a Windows machine whose test folder passes the access tests.

**Elapsed**: unknown. **Tokens**: unknown.

## Strategy's direct checks before code review -- Claude Fable 5.2 (Strategy) -- 2026-11-21

The Windows-only tests cannot run on this machine, so Strategy checked (a) to (d) directly, on the branch at `5aa8f5ce`. All four behave as the plan says.

**Why the native tests fail here** (two causes found, one not). Under the default temp folder the first refresh answers `unavailable`: an app-capability identifier holds full control of `AppData`, which the meter's access test refuses on the way to the test's folder (read with `Get-Acl`). From a temp folder on a path the meter accepts, the same refresh answers `git_parser_failed`. The meter's own Git helper reads a made-up project's remote correctly from such a path with the machine's real Git, so that cause lies in the tests' stand-in Git, and it is not found. It is not the project's folder on the `F:` drive: the tests work in a temp folder on `C:`.

**Five planted cases, through the real `_enumerate_windows_jsonl` and the real Windows calls,** on made-up files in a throw-away folder on a path the meter accepts. Run once with the meter of `0.9-dev` and once with this branch's:

| Case | Before | After |
|---|---|---|
| A sub-folder that reports 4,096 bytes, holding a log | refused, `source_changed` | accepted, 2 logs |
| A log with a second name outside the folder | refused, `source_read_unavailable` | accepted, 1 log |
| A log with both names inside the folder | refused, `source_read_unavailable` | refused, `source_read_unavailable` |
| A log with a second name that the Users group may write | refused, `source_read_unavailable` | refused, `unavailable` |
| A log with one name that the Users group may write | accepted | accepted |

The fourth row is the planted bad input for the new access test: it is refused. The fifth is not changed by this plan and is shown for comparison. The cases use plain folders: a folder made by Python's `tempfile.mkdtemp` carries an access list of its own, which the walk refuses.

**A real refresh with this branch's meter on the Windows Server machine** (reason codes and code locations only). It gets through the walk and the reader over 137 log files, with no `source_changed`, no `source_read_unavailable` and no failed lookup. Its only refusals are the access test on the project's folders on `F:`, and the receipt is `project_remote_unavailable`, which is the Maintainer's to settle.

**Reply times on a real log.** Two refreshes with this branch's meter around a short stretch of one session: 1 reply, written as 2 records with different times. The meter recorded 1 event with its time known and no `ambiguous_time`, and its token totals by kind equal an independent count (output 1,202; cache read 548,108). A longer stretch, with sub-agent runs in it, is checked after the code reviews.

Not checked: the native test's new last stage and the `hardlink` case as tests, which have not passed anywhere since the change; the Mac and Linux paths.

**Elapsed**: unknown. **Tokens**: unknown.

## Code review -- Claude Sonnet 5.5 (usual reviewer) -- 2026-11-21

Reviewed range: `02dfe045e669ecc326ec129b7b25ba6aa6f01bc9` (merge base with `0.9-dev`) to `d8f675d5485494eff768d8903cd6351504f0ae9d`; code ends at `fb400b49`.

**Obligation**: usual code review. Status left as is for the Security Review pass.

**Verdict**: ACCEPT. Conditions (a) to (d) are as the plan states and nothing else in `meter.py` changed. No blocking finding.

**Foundations**

1. **Should this happen as framed?** Yes: the diff of `dev/tools/meter.py` is 22 lines, in the three named places only -- `git diff 02dfe045 HEAD -- dev/tools/meter.py`.
2. **Best alternative.** None simpler; changing two existing tests instead of adding three keeps the frozen files untouched -- `git diff --stat` on `tests/security_manifest.py` and `tests/test_security_check.py` is empty.
3. **What would show it wrong.** A Windows run where the fixture's first refresh answers `ok` and the new last stage fails; Strategy's real refresh -- plan "Strategy's direct checks".

**Findings**

1. Non-blocking: the time test fails if (d) is wrong either way. The three copies are dated 12:00:02, 12:00:00 and 12:00:05; keeping the first (02), the last (05) or losing the time all fail an assertion. It does not test text order against instant order (an offset time); the `fromisoformat` key is read, not run on such a case.
2. Non-blocking: the native stage fails if (a) or (b) is wrong (refresh not `ok`) or (c) refuses the second name. It would not catch a file read twice, since `_merge_event_batches` keeps one event per key. Reading twice is covered by `seen` in code and by Strategy's planted case 3, not by a test.
3. Non-blocking: the native stage cannot run on this machine; it and `hardlink` have passed nowhere since the change. The `hardlink` case is unedited (not in the diff). Strategy's planted cases cover (a) to (c) through the real walk; they do not cover (b)'s "folder changes during a refresh" cost.
4. The fixture fix copies `pulse.py` with the same byte check; nothing else in the set-up changed. Copies: `cmp` prints nothing; the lock commit holds only `dev/.cairn/cairn-lock.yml`; `verify_integrity.py` reports OK. README and changelog lines match what shipped. The record says what was and was not run.

I ran the time test once: passed.

**Not covered**: the Windows-only tests; Security Review questions; real logs; the Mac and Linux paths.

Elapsed time: unknown. Tokens: unknown.

## Code review -- Claude Opus 5.5 (Security Review) -- 2026-11-21

Reviewed range: `02dfe045e669ecc326ec129b7b25ba6aa6f01bc9` (merge base with `0.9-dev`) to `8d91e35f534a765e13d0c7a980bbc35d191538a3`; code ends at `fb400b49`.

**Obligation**: Internal Security Review. No blocking finding in either review, so Status stays.

**Verdict**: ACCEPT. I agree with the usual review's findings 1 to 4; on the security questions below, my wording governs.

**Foundations**

1. **Should this happen as framed?** Yes: each other check on the walk and the reader is unchanged; only the size test (folders), the folder reading, the link tests and the merge loop moved -- `git diff 02dfe045 fb400b49 -- dev/tools/meter.py`.
2. **Best alternative.** None safer at this size; the `profile` test denies every other account write, append, attribute, access-list and owner rights -- `check_acl`, `dev/tools/meter.py` lines 656-657.
3. **What would show it wrong.** A two-name file that another account may write being read; Strategy's planted fourth case shows it refused -- plan "Strategy's direct checks".

**Answers.** A planted name for a file another account can write is refused (`profile`). One file is never read twice in one walk: `seen` refuses a second meeting, and a link added mid-walk changes a folder's write time, which `verify` catches. The file read is tied to the file accepted by volume and file id at open and close (`_check_stream_identity`); its access list cannot be loosened by another account, since both tests deny it that right. (d) compares only records in one file read, all timestamps carry a zone, so no one without write access can move usage between days. (a) and (b) keep identity and directory checks; `verify` still compares each folder's write time and size.

**Findings**

1. Non-blocking: a co-user who may add files to the log folder (the `ancestor` test allows it) can still plant a name for a user-owned file it can open but not write, such as a log outside the approved roots. No usage can be invented, since the content is the user's own; at worst real usage from outside an approved root is counted. The plan's "a second name outside the folder gives a reader no content the log does not already hold" holds only for names the user's app made. Before this change such a name was refused.
2. Non-blocking: removing the reader's link test also reaches the Git helper's read (line 5911), which has no walk; its SHA-256 check keeps it safe.

I ran the time test once: passed. `cmp` printed nothing; `verify_integrity.py` reports OK; the frozen files are untouched.

**Not covered**: whether Windows lets an account link a file it cannot write (not tested); the Windows-only tests; real logs; Mac and Linux.

Elapsed time: unknown. Tokens: unknown.
