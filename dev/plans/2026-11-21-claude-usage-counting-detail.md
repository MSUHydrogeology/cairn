# Plan detail: Count Claude usage toward a project

This is the companion of `dev/plans/2026-11-21-claude-usage-counting.md` and part of it. It holds the exact names, conditions, reason codes and test inputs, so that a low-tier agent invents no design. It exists because the opening plan would otherwise pass 1,500 words. Every code change lands in both copies of the meter (`dev/tools/meter.py` and `templates/skills/_lib/meter.py`); the second is made by copying the first (`cp`) in the same commit, then `cmp` of the two must print nothing.

Proposed paths:
- `tests/test_meter_claude_usage.py`

Names that carry no vendor word are chosen on purpose, so the neutrality lint needs no marker. The existing `# vendor-ok:` markers stay where they are. A new line that must repeat the quoted tool name is avoided.

## D0. Names and numbers that are fixed here

- Reason code (new, kept off `_PULSE_BENIGN_REASONS` in `dev/tools/pulse.py`, which is not edited): `agent_runs_incomplete`.
- Ledger field (new): `agent_runs`, a dict with exactly the keys `transcripts`, `summaries`, `unclassified`.
- `READER_VERSION = "cairn-source-readers/6"`. `LEDGER_SCHEMA = "cairn-meter-ledger/6"`. `_OLD_LEDGER_SCHEMAS` gains `"cairn-meter-ledger/5"`. An old ledger is then refused with `ledger_old_schema`, as the two earlier versions were, and the README's existing sentence says what to do.
- Constants next to the other `MAX_` lines: `MAX_AGENT_SUMMARIES = 1_000`, `MAX_AGENT_TRANSCRIPTS = 100_000`, `MAX_SUMMARY_NAMES = 256`.
- `_SUMMARY_FIELDS = frozenset({"total_tokens", "tool_uses", "duration_ms"})`. **Not confirmed against a real record**: the agent that wrote this plan may not read provider logs. The names are the wording Claude Code uses for a sub-agent's totals. Strategy's check P1 (below) confirms them, and replaces them here by exact replacement if they differ, before C2 starts.
- Record keys read: `type`, `message`, `message.id`, `message.model`, `message.usage` and its existing fields, `sessionId`, `requestId`, `cwd`, `timestamp`, plus two new ones, `isSidechain` and `agentId`. The same two are on the allowed-name list of D6. Strategy's check P2 confirms the two new ones.

## D1. The folder rule (C1)

New function `_project_for_folder(cwd, projects)` in `meter.py`, placed after `_codex_context`. It returns the one project dict whose path contains `cwd`, or `None`. It never opens a folder. Steps, in order:

1. `cwd` must be a `str` and pass `_text` (non-empty, at most 4096 characters, no character below 32 and no 127); otherwise return `None`.
2. If `os.name == "nt"`: call `_windows_absolute_parts(cwd)` (drive letter, backslashes only, no leading two backslashes, no `/`, no empty part); on `Unavailable` return `None`. The separator is `"\\"`. Otherwise: `cwd` must start with `/` and no part of `cwd.split("/")` may be `.` or `..`, else `None`. The separator is `"/"`. This is the Codex test (`_codex_context`), repeated, not shared, because the Codex tests pin that function.
3. A project contains `cwd` when `cwd == project["path"]`, or when `prefix = path if path.endswith(sep) else path + sep`, `cwd.startswith(prefix)`, and the rest `cwd[len(prefix):]` is non-empty and `all(rest.split(sep))` (no empty part). No case folding, no trimming, no `..` resolution, no link or drive lookup.
4. Return the project when exactly one contains `cwd`; none or two or more return `None` (a folder inside two configured projects counts for neither).

## D2. The Claude branch of `read_records` (C1)

Changes inside the block that begins `if tool == "claude":  # vendor-ok: ...`, assistant records only:

- `event_key = _digest(tool, response, message_id)`: the session leaves the key. `response` is still the request id, or the message id when the record has none.
- Replace `reasons = {"project_path_unapproved"}` with this, in order:
  - `reasons = set()`; `bound = None`; `folder_project = _project_for_folder(record.get("cwd"), projects) if source_root_approved else None`.
  - `request is None`: add `conflicting_binding` (a record with no request id is never proven).
  - else if `account_filter_requested`: nothing here (the existing later line adds `account_filter_unproven`).
  - else if `folder_project is None`: add `project_path_unapproved`.
  - else: look up `(alias, path)` in `verified_projects`; if absent, `verified_projects[key] = verify_project(folder_project, excluded_roots)`. With `(remote, reason)`: `reason is None` sets `bound = folder_project`; otherwise add `reason`.
  - The existing `usage_invalid or model_invalid` line then adds `invalid_record`.
- `_event_record(...)` gains `project_alias=bound["alias"] if bound else None`, `project_state="current_local_verified" if bound else "unknown"`, `ownership="proven" if bound else "unknown"`. Nothing else in the call changes.
- Under a failed account filter the kinds go unknown as today; `bound` stays `None` in that case.
- Two sightings of one message under two sessions, two folders, or one folder and no folder differ in `thread_key`, `session_key`, `session_digest`, `project_alias`, `project_association` or `ownership`, which the existing merge at the end of `read_records` already turns into `conflicting_binding` and an unknown event. Nothing is added for this; the test in D5 proves it.

## D3. Summaries and transcripts at read time (C2)

1. Replace `_record_carries_usage` by `_usage_values(record)`: the same non-recursive walk (a list used as a stack over dict values and list items), returning the list of every value stored under a key named `usage`, descending into every value including that one.
2. New `_summary_names(record)`: returns `None` unless `values = _usage_values(record)` is non-empty and every value is a `dict` with `set(value) == _SUMMARY_FIELDS` whose three values each pass `_counter` (a whole number, not a boolean, from 0 to `MAX_COUNTER`). If it passes, walk the record again (same stack) over string values only (never keys), find every maximal run `(?<![A-Za-z0-9])[A-Za-z0-9]{8,64}(?![A-Za-z0-9])`, keep a run only if it holds at least one digit and at least one letter, and collect `_digest("agent-id", run)` of each into a set. Return `[]` when the set holds more than `MAX_SUMMARY_NAMES`, else the sorted list. An empty list means "names no agent", and the ledger will hold the summary as uncovered.
3. The non-assistant branch becomes: a `kind` in the four skipped names (`user`, `system`, `progress`, `file-history-snapshot`) is skipped first, before any look at usage, exactly as today. Any other record with an empty `_usage_values` is skipped silently, as today. Otherwise `names = _summary_names(record)`. If `None`: `issues.add("agent_runs_incomplete")`, `unclassified += 1`, `continue` (never `unsupported_record`). If a list: read `session_key = _digest(tool, _text(record["sessionId"]))`; when `sessionId` is missing or fails `_text`, treat the record as the `None` case (same issue, one more `unclassified`). Otherwise keep `(session_key, tuple(names))` in a set.
4. In the assistant branch, after `session` is read: if `record.get("isSidechain") is True`, and `_text(record["agentId"])` succeeds, keep `(session_key, _digest("agent-id", agent_id))`, where `session_key` is `_digest(tool, session)`. A failure to read `agentId` keeps nothing and changes nothing else; the event is still read.
5. The batch returned by `read_records` gains `"agent_runs": {"transcripts": [...], "summaries": [...], "unclassified": n}`, the lists sorted, unique, as dicts `{"session_key", "agent_key"}` and `{"session_key", "names"}`. It is `_empty_agent_runs()` for the other tools. When `lines.terminal_reason` is set, or the candidates exceed `MAX_NORMALIZED_EVENTS`, the three parts are emptied together with the events.
6. The old test of an unknown record type with `usage` changes its expected code (D5). The reason `unsupported_record` stays for the Codex branch.

## D4. The ledger's memory and the version change (C3)

- `_empty_agent_runs()` returns `{"transcripts": [], "summaries": [], "unclassified": 0}`.
- `_merge_agent_runs(first, second)` returns a new dict. Steps: union the transcripts (pairs of the two keys) and the summaries (`(session_key, tuple(names))`); add the two `unclassified` counts, at most `MAX_COUNTER`. A summary is covered when exactly one of its names equals the `agent_key` of a transcript with the same `session_key`; drop covered summaries. If more than `MAX_AGENT_SUMMARIES` remain, or more than `MAX_AGENT_TRANSCRIPTS` transcripts, keep the first ones in sorted order and add the number cut to `unclassified` (the meter never fails a refresh over this; it says INCOMPLETE). Return sorted, unique lists in the row shapes of D3.5.
- `_validate_agent_runs(value)` (raises `ValueError`): the three keys exactly; every key and name a 64-character lower-case hex string; both lists sorted and unique; the caps above; `unclassified` passes `_counter`.
- `_LEDGER_FIELDS` gains `"agent_runs"`. `_load_ledger(None)` returns `agent_runs: _empty_agent_runs()`. `_load_ledger(raw)` calls `_validate_agent_runs(ledger["agent_runs"])` after the aggregate rows, inside the existing `try`.
- `_scan_approved_sources(..., agent_runs=None)`: a keyword-only parameter, last. When it is a dict, after each batch is appended, `merged = _merge_agent_runs(agent_runs, batch["agent_runs"])`, then `agent_runs.clear()` and `agent_runs.update(merged)`. When `None`, nothing changes. The return value is unchanged (seven values).
- `_new_ledger(..., now=None, agent_runs=None)`: `runs = _merge_agent_runs(prior["agent_runs"], agent_runs or _empty_agent_runs())`; the returned ledger holds `"agent_runs": runs`; after `reasons = set(scan_reasons)` add `agent_runs_incomplete` when `runs["summaries"]` is non-empty or `runs["unclassified"] > 0`.
- Both refresh functions (`_refresh_ledger`, and `build_candidate` inside `_refresh_ledger_windows`): `runs = _empty_agent_runs()` before the scan, `agent_runs=runs` passed to the scan, `agent_runs=runs` passed to `_new_ledger`.
- Nothing is read from `agent_runs` by `_project_export`: the reason reaches every export through `coverage.reasons`, and `pulse.py` prints INCOMPLETE for any reason not in its benign list.
- A fresh ledger counts nothing before its first refresh (the existing "start" rule). So a meter that has just been moved aside records where each log ends and counts only what is written afterwards.

## D5. The tests (hand-written records only; no provider log is read)

All new tests are in a new file, `tests/test_meter_claude_usage.py`, listed in `tests/test_tiers.json` in C1 (same tier as `tests/test_meter_usage_free_records.py`), except the three changed ones and the two end-to-end ones, which are in `tests/integration/test_meter.py`. Helper in the new file: `rec(**changes)` builds an assistant record in the shape of `claude()` in `tests/integration/test_meter.py` (copy its key names), with `cwd` set to the project path; `cfg(paths)` builds a config with one source root and one project per path; `read(records, cfg, root)` calls `meter.read_records("claude", encoded, config=cfg, source_root=root)` with `meter._verified_project_remote` patched to return `(project["remote"], None)`. Host paths are built with `"C:\\synthetic\\..."` on Windows and `"/synthetic/..."` elsewhere.

**C1 tests** (each failing case has the passing control beside it):

| Test | Input | Expected |
|---|---|---|
| inside_counts | `cwd` equal to the project path; control: `cwd` a sub-folder | `project_alias` set, `current_local_verified`, `proven`; no `project_path_unapproved` |
| outside_stays_unknown (parametrized) | outside the project; sibling `<path>-old`; trailing separator; project path with letters re-cased; a `..` part; a relative path; a control character; an empty part after the path | unknown event, `project_path_unapproved`, kinds still read |
| windows_forms (monkeypatch `meter.os` to `SimpleNamespace(name="nt")`, call `_project_for_folder`) | `C:/synthetic/p`; `\\\\host\\share\\p`; `C:\\synthetic\\p\\` | `None` each; control `C:\\synthetic\\p\\sub` returns the project |
| inside_two_projects | projects `P` and `P\\inner`, `cwd` inside `inner` | unknown, `project_path_unapproved` |
| remote_fails | patched check returns `(None, "project_remote_mismatch")` | unknown, that reason, no project |
| source_root_unapproved | `source_root` not in the config | unknown, `project_path_unapproved` |
| no_request_id | no `requestId`, project configured | `ownership` unknown, `conflicting_binding` |
| two_sessions_one_message | same ids, different `sessionId`, both inside | one event, `conflicting_binding`, unknown, no project; control: same session twice, equal usage: one event, `proven` |
| two_folders_one_message | same ids, one record inside project A and one inside project B (two projects), then A and outside | one event each time, `conflicting_binding`, unknown |
| repeats_differing_usage | same ids, equal folder, `output_tokens` 4 and 5 | kinds unknown, `conflicting_usage`; control equal usage merges |
| same_log_two_roots | the same records read as two batches with two aliases, joined by `_merge_event_batches` | one event |

Edited in `tests/integration/test_meter.py` (C1): `event_key_for` returns `meter._digest("claude", "request-" + message_id, message_id)` and keeps its `session` parameter unused.

**C2 tests** (new file):

| Test | Input | Expected |
|---|---|---|
| summary_is_not_usage | an `attachment` record with `usage` of exactly the three fields, ints, plus a `sessionId` and a text holding one id-shaped word; control: the same record with `type` `user` | no event, no `unsupported_record`, no `agent_runs_incomplete`, one summary row; the control: empty `agent_runs`, `issues == []` |
| summary_shape_fails (parametrized) | a wrong field name; an extra field; a missing field; `-1`; `True`; `1.5`; `"3"`; `usage` nested in `usage`; `usage` a list; `{}`; one good and one bad `usage` in one record | `agent_runs_incomplete` in `issues`, `unsupported_record` not, `unclassified == 1`, no summary row |
| skipped_types_stay_skipped (parametrized over the four names) | a summary-shaped and a malformed `usage` | `issues == []`, empty `agent_runs` |
| summary_without_session | valid shape, no `sessionId` | `agent_runs_incomplete`, `unclassified == 1` |
| names | text with one id-shaped word; none; the same word twice; 257 different id-shaped words; a 65-character run | one name; `[]`; one name; `[]`; `[]` |
| transcript_registered | assistant with `isSidechain` true and an `agentId`; control: no mark; mark with a bad `agentId` | one pair; none; none, and the event is still read |

Edited in `tests/test_meter_usage_free_records.py` (C2): `test_unknown_record_type_with_usage_is_unsupported` now expects `"agent_runs_incomplete" in issues` and `"unsupported_record" not in issues`; its name becomes `..._is_flagged_incomplete`. The two usage-free tests and the four-names test stay as they are.

**C3 tests** (new file unless stated):

| Test | Input | Expected |
|---|---|---|
| summary_then_transcript | `_new_ledger` with a summary naming agent X; then a later `_new_ledger` with the transcript of X, same session | first ledger has `agent_runs_incomplete`; the second has no such reason and no summary row |
| not_covered (parametrized) | transcript under another session; summary naming two transcripts; summary naming none | reason present |
| resumed_agent | two summaries naming X, one transcript | covered, no reason |
| unclassified_is_sticky | one ledger with `unclassified == 1`, then a clean refresh | reason still present |
| caps | 1,001 uncovered summaries (monkeypatch the cap to 3 for speed) | cut, `unclassified` grows by the number cut, refresh does not fail |
| ledger_roundtrip_and_refusals | `_load_ledger` of a ledger holding runs; hand edits: unsorted list, a duplicate, a non-hex key, 257 names, a negative count, an extra key | round trip equal; each edit `ledger_invalid` |
| empty_ledger | `_load_ledger(None)` | has `agent_runs` |
| export_reaches_pulse | a ledger with the reason, `_project_export_bytes`, then `pulse._parse_meter_aggregate` | `incomplete_reasons` holds `agent_runs_incomplete` |
| end_to_end_counts (`tests/integration/test_meter.py`, POSIX only, built on `c1_home`) | refresh once (start), then add a log whose records have the project folder, a transcript file and a summary naming it; refresh | the export has Claude rows whose kinds equal the hand sum; no `agent_runs_incomplete` |
| end_to_end_incomplete (same file) | as above but no transcript, refresh; then add the transcript, refresh | the first export lists the reason; the second does not |

Edited in `tests/integration/test_meter.py` (C3): the four places that name `cairn-meter-ledger/5` or `cairn-source-readers/5` now name `/6`; `test_an_old_ledger_is_refused_and_never_overwritten` gains the pair `("cairn-meter-ledger/5", "cairn-source-readers/5")` and deletes `agent_runs` from the old ledger for all three pairs, while the existing deletions of `starts`, `fold_horizon`, `daily` and the cursor fields apply only to the `/3` and `/4` pairs.

## D6. Rule, docs and records (C4)

- `dev/rules/custom_session_routines.md`: after the sentence that ends "never create or edit it without the Maintainer's clear yes.", add: "Nothing read from a provider log goes into a plan, test, fixture, commit, report, chat reply or agent prompt except counts, the meter's own sanitized output, and field names on the list kept in this file; any other field name is counted, never shown." Then a short heading "Field names that may be shown" with one list: `type`, `message`, `id`, `model`, `usage`, `sessionId`, `requestId`, `cwd`, `timestamp`, `isSidechain`, `agentId`, `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `cache_creation`, `ephemeral_5m_input_tokens`, `ephemeral_1h_input_tokens`, and the three in `_SUMMARY_FIELDS`. The list is the keys the reader reads, nothing more.
- `dev/measurement/README.md`: in the Meter paragraph, after the `ledger_old_schema` sentence, add two sentences: a Claude record counts toward a project when its own working folder is the project's or lies inside it, its log is under an approved root and the project's remote checks out; summaries of finished sub-agents are not counted, and a reading whose summaries cannot be tied to a read transcript prints INCOMPLETE. The shipped `templates/core/dev/measurement/README.md` holds no such paragraph; it is not edited.
- `CHANGELOG.md`: one Major entry under `## Unreleased`, "Added: Claude usage counts toward a project." One or two plain sentences, a link to this plan, in Keep a Changelog order (after the existing Changed entry).
- `dev/PLANNING.md`: only the two links to the proposal's old place are repointed (already done in the opening commit). C4 adds nothing there; the closeout names what remains.

## D7. Strategy's checks (counts only; the build agent must not attempt them)

Before C2 starts (private logs; Strategy reads, prints counts only):
- **P1.** Every `usage` dict in records that are neither assistant nor one of the four skipped types has exactly the key set in `_SUMMARY_FIELDS`; the count is 84 of 84 on the measured project. If the names differ, replace D0 and D3 by exact replacement.
- **P2.** On every assistant record of every transcript, `isSidechain` is `true` and `agentId` is a string; on the main log's own records neither is present.
- **P3.** Every transcript agent id is one maximal run of 8 to 64 letters and digits with a digit and a letter; and, by D3.2's rule, each of the 84 summaries names exactly one transcript's id. The largest number of distinct runs in one summary is at most 256 (else raise `MAX_SUMMARY_NAMES`).

After C3, before code review: **the developmental check on a real log.** The Maintainer or Strategy moves the old ledger aside (the README's own step, choice 5), refreshes once to set the start, uses Claude for one session, refreshes again, and compares the meter's per-kind sums for that session with an independent count-only sum of its log and transcripts. Nothing counts before the first refresh, so an old session cannot be the one checked. On this Windows host the refresh runs through the native route; the end-to-end tests above are POSIX only.
