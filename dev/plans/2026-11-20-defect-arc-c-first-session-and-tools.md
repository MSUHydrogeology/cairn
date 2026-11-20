# Plan: Defect arc C, first session and tools

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-20
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/certifying-runs.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: Fix what adopters met in a first session and in two tools: session start lists README files as work and prints Windows paths with `\x5c`, the intent hook misreads Windows files, the usage meter marks usage-free records as unsupported, and the security audit gets a threshold the adopter sets.

## Build summary

After this plan, session start on a fresh Windows install lists no README as open work, prints paths with forward slashes, no longer edits `.gitignore` when a broader rule already covers the skills folder, and names both shell forms when it refuses a full handoff. The intent pre-commit installer stops calling every Windows shell hook non-executable. The usage meter stops listing usage-free Claude record types as unsupported. The security audit reads an optional threshold file the adopter owns and prints the threshold on every result; with no file it behaves as today. Four chunks fix shipped Python; the fifth refreshes Cairn's own records. Two findings change what the plan can promise, and are in Scope.

## Source proposal

The Maintainer accepted the defect arc at the heavy tier ("Go ahead on the defect arc.", chat, 2026-11-20). Plan C is its first-session and tools part: #98 parts 1 and 2, #91 part 2, #96, #99 part 6 with #101, and three defects found since (the roadmap's "Add any defect found since"). This plan executes it and reopens nothing. It takes a usual review and a Security Review, at plan stage and again at code stage. Exact message texts, algorithms and fixtures are in the companion file `dev/plans/2026-11-20-defect-arc-c-first-session-and-tools-detail.md` ("Detail" below), so a low-tier implementer has no design to invent. The companion is part of the plan.

## Scope

**Result.** A first session on a fresh Windows install shows true orientation text, and the two tools do what their issues ask without widening any check.

Proposed paths:
- `tests/test_session_first_session.py`
- `tests/test_intent_precommit_classify.py`
- `tests/test_meter_usage_free_records.py`
- `tests/test_security_audit_threshold.py`

| Item | Chunk | Entry point |
|---|---|---|
| #98.1 README; #98.2 slashes; `.gitignore` edit; handoff message; one comment | C1 | `session.py session-start`, `session-end --handoff` |
| #91 part 2 execute bit; one comment | C2 | `intent.py install-precommit` |
| #96 usage-free records | C3 | `meter.read_records`, `meter.py refresh --report --json` |
| #101 threshold; #99.6 finding | C4 | `run_security_audit.py` |
| One comment, changelog, own lock | C5 | `verify_integrity` |

**Where the code differs from Strategy's defaults** (read, not run unless stated):
1. **#96 will not change the Pulse's UNKNOWN.** `coverage.usage` is PARTIAL only when `project_usage.aggregates` holds a row for the tool (`pulse.py`, `build_pulse`). `_project_export` keeps only events that are `proven` and `current_local_verified` (`meter.py`, near line 3717). Claude events are built with neither: the reader never sets them, and its test fixture calls the folder "not-proof". So Claude stays UNKNOWN even when every record type is accepted. C3 delivers what the proposal names (usage-free types stop raising `unsupported_record`). Whether Claude usage should count toward a project is a trust decision, not made here (question below). Measured on this machine's current log (counts only): 1 file, 7,895 records, 17 record types; 13 are outside the adapter's allowed set; one of them is not among the 18 the issue lists, so a closed list goes stale. None carries a `usage` key. All 1,837 assistant usage records parse. The reporter's 10 rejections do not reproduce here.
2. **#91 part 2.** Only the pre-commit classifier tests the execute bit (`_classify_existing_precommit`). The post-commit path uses `os.access`, which works on Windows. The four tests the issue names exist nowhere in the tree or in `templates/` (searched by name): they are not Cairn's.
3. **#101.** The dispatcher never runs the audit, so "the dispatcher record carries the threshold" does not apply. The audit's own pass line and summary carry it.
4. **#99.6, why an adopter's audit sees Cairn's tools.** It does not. `run_bandit_pass` scans only `python_package`, and `run_adopted_executable_gate` checks hashes, not code. The twelve findings came from the adopter's own whole-tree test. Cairn already allows the same `exec` findings, and the twelfth (`pulse.py`, B314), in its own gate (`ALLOWLIST` in `release/security_check.py`); adopters have no such list. Nothing in the audit changes for this.
5. **`.gitignore`.** Git's `check-ignore` is not an allowed form of the pinned Git helper, which this plan does not change, so a small text matcher decides (Detail D3).
6. **Comments.** Taken, comment text only: `session.py` line 127 (both copies), `intent.py` line 56 (both), `measurements.py` line 19. Left: comments in frozen files not otherwise edited (`measurements.py` is the one exception: the HOLD is taken because the comment misleads adopters) (`claim_check.py`, `content_scan.py`, `content_scan_runner.py`, `run_portable_security_sweeps.py`, `run_security_verification.py`, `api_access_security.py`; each would add a signing HOLD for a comment). Home: plan D, which edits frozen files. Docstrings and strings that name old folders stay, because changing them can alter recorded baselines.

**Protected files and the reason the Maintainer will see at the signing.**
- `templates/skills/_lib/session.py` and `dev/tools/session.py` (interpreter-binding reader, byte copies; not frozen): display and read-only listing fixes, and one fewer write; no check widened.
- `templates/modules/team-gated/_intent/conflict.py` and `dev/tools/_intent/conflict.py` (frozen, HOLD): the pre-commit installer stops calling Windows shell hooks non-executable; POSIX unchanged.
- `templates/modules/team-gated/run_security_audit.py` (frozen, HOLD): the audit takes an adopter-set threshold from one closed-format file; default unchanged; unknown input degrades.
- `meter.py` (both): usage-free records stop marking Claude logs incomplete; a usage-bearing record of an unknown type still does.
- `intent.py`, `python-security.md`: comment or prose only.
- `templates/modules/default-on/measurements.py` (frozen, HOLD): one comment names `dev/tools/`; no code changes.
- `dev/.cairn/cairn-lock.yml`: four records refreshed by the repository's own tool (C5).

**Staleness (read, not run).** Nothing under `install/_scaffold/` changes, so the AST baseline stays valid. The gate manifest freezes three files changed here: `conflict.py`, `run_security_audit.py` and `measurements.py` (listed there as `scripts/measurements.py`); the verifier will show three HOLDs. Reason for the third: one comment now names `dev/tools/`; no code changes. Not run. The install lock goes stale after C1 to C3 and is refreshed in C5.

**Reuse.** `encode_display`, `_assert_not_linked`, `_write_replacing` (kept); `run_bandit_pass` and `_run_tool` (extended, not duplicated). Searched `dev/tools` and `templates` for `check-ignore`, `min_severity` and `usage` readers: none does these jobs.

**Question for the Maintainer.** After C3 the Pulse still shows Claude usage as UNKNOWN and the goodnight report still has no Claude numbers, because the meter never ties a Claude record to this project: it does not trust the folder a log sits in. Should it? Yes counts Claude usage once the folder matches the project; no keeps today's strict refusal. Default: no change now; decide in the tightening or v0.10.

### Documentation / doctrine surface

`python-security.md` (module page) and `CHANGELOG.md`. No doctrine rule changes.

## Sequence

C1 to C4 touch disjoint files and can land in any order. Code review once after C5. No earlier review point: nothing builds on a chunk. C5 needs C1 to C3 committed (it hashes their files). Its changelog lines are inserted next to plan B's by exact insertion, never regenerated.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Session start | plan review | README skip, forward slashes, `.gitignore` check, handoff text (#98.1, #98.2, two found since) |
| C2 | Intent hook | plan review | Windows execute-bit test (#91.2) |
| C3 | Usage meter | plan review | usage-free record types (#96) |
| C4 | Audit threshold | plan review | policy file, JSON verdict, printed threshold (#101, #99.6) |
| C5 | Records | C1 to C3 | comment, changelog, own lock |

## Acceptance criteria

**C1.** (a) `session-start` on a tree whose `dev/proposals/` and `dev/plans/` hold `README.md` (any letter case) lists neither; real files and the status advisory are unchanged (`_in_flight_items` skips the name case-insensitively). (b) On Windows the line `interpreter:` and the other path messages print `C:/...`, never `\x5c`. New `encode_display_path(value)` replaces backslashes with `/` only when `os.sep` is a backslash, then calls `encode_display`. `encode_display`, its table and child-output encoding are untouched, so a backslash still prints as `\x5c` on POSIX and in child output. It replaces `encode_display(str(path))` at the twelve path sites in Detail D2. (c) New `_gitignore_covers(text, entry)` (Detail D3) stops a seed when `.claude/` already ignores the folder; a file with any `!` line, or an unrecognized rule, still gets the line as today. (d) The refusal at the handoff gate names the bash and PowerShell forms (Detail D4); it still contains "no maintainer-designation marker". (e) `session.py` line 127 names `tests/`. **Permanent**, in `tests/test_session_first_session.py`, through `main(["session-start"])` and a copy fixture: README skipped; slashes on Windows (skipped elsewhere with a reason); `.gitignore` byte-identical under `.claude/`, line added under an unrelated rule or a `!` line; `encode_display("a\\b")` still `a\x5cb`. **Developmental:** read the handoff refusal in bash and PowerShell; no wording is pinned.

**C2.** `_classify_existing_precommit` (both copies) tests the execute bit only when `os.name != "nt"`. Git for Windows runs hooks through its own shell and Windows files have no bit. POSIX stays bit-for-bit (a plain `os.access` would change it). **Permanent**, `tests/test_intent_precommit_classify.py`, through `intent.py install-precommit`: a shell hook with mode 0o644 is refused (exit 4, file unchanged) and the message says `non-executable` on POSIX and `foreign` on Windows; fails before the fix on Windows. The label is the reported promise, so the test pins it. The four named tests are recorded as not Cairn's, with the search as evidence; closing the issue is the Maintainer's.

**C3.** In the Claude branch of `read_records` (both copies), a non-assistant record sets `unsupported_record` only when it is not one of the four existing names and `_record_carries_usage(record)` is true: a `usage` key in any dict anywhere in the record (Detail D6). Else it is skipped silently. An assistant record with unreadable usage still sets `invalid_record`. **Permanent**, `tests/test_meter_usage_free_records.py`, through `read_records`, hand-written records only (Detail D6): usage-free types leave `issues == []` and the event; an unknown type with `usage` raises `unsupported_record`; a bad assistant usage raises `invalid_record`. **Developmental, this machine only, nothing copied:** `read_records` over the current log reports `unsupported_record` at the starting commit and not after; delete the script.

**C4.** `run_bandit_pass(pkg, repo_root)` keeps its signature. It loads the optional policy file (Detail D7); prints the threshold line first; if both minimums are `low` (or no file), runs today's argv and today's verdict unchanged. Otherwise it adds `-f json` and classifies the parsed findings: a finding fails when severity and confidence are each at or above the minimum; an unknown level fails. Below-threshold findings are printed (the JSON) and counted. Clean-below-threshold returns tier 0 with status `bandit:clean-below-threshold`; every non-default status that is not DEGRADED gets the suffix ` [threshold: ...]`, so the summary shows it; DEGRADED statuses carry no suffix. A bad policy file, unparseable output, code 0 with findings, code 1 without, or any code other than 0 or 1 is DEGRADED (20). No flag, no environment variable. **Permanent**, `tests/test_security_audit_threshold.py`: the cases in Detail D7, stubbing `_run_tool` as `tests/test_security_stack.py` does; one real-Bandit case skipped when Bandit is absent. The existing audit tests stay untouched and must pass.

**C5.** `measurements.py` line 19 names `dev/tools/`. One Fixed and one Added changelog line (extend an Unreleased entry on the same topic if one exists). Scoped `upgrade --finalize` over `dev/tools/session.py`, `dev/tools/_intent/conflict.py`, `dev/tools/meter.py`, `dev/tools/intent.py`; `verify_integrity` reports OK for all recorded files; the lock commits alone. Twins stay byte-identical (checked by `cmp`).

**Security (re-answered).** S1: the policy file, the log records and the `.gitignore` are adopter-supplied; each reader has a closed shape and refusal, and none echoes a raw value; only the policy file gets a size cap (D7), and the `.gitignore` reader gets no new size cap. S2: negative controls are the `!` line, the unknown-type record with usage, the bad usage record, and each policy refusal. S3: `session-start`, `install-precommit`, `meter.py refresh`, and `run_security_audit.py` fire the checks. S4: no default lands on more authority; a malformed policy degrades, an unknown level fails, and no check accepts more by default. S5: someone who writes the policy file can lower what fails; every result prints the threshold and counts below-threshold findings. A tool that lies about a usage field is out of scope.

## Scope delta

**Scope delta**: preserved. Every outcome the proposal gives plan C is delivered, #96's wording included (the cause named is removed); the UNKNOWN that remains is shown above to have another cause.

## Verification

**Selector** (`C:\ProgramData\Anaconda3\python.exe tests/tier_inventory.py for <paths>` at `02f92d37`, before any new test file): C1 42 files, C2 23, C3 8, C4 5, C5 7; each of C1 to C4 adds one. For each chunk run its selected files once at the starting commit and keep each failure's test id and message; run them again after; a failure is a host failure only if both are on the first list. One exception, by design: `test_session_failsafe.py::test_interpreter_resolved_from_local_env_and_reported` expects a backslash path, so on Windows it fails before C1 (the line shows `\x5c`) and after (it shows `/`), with different text. It is frozen and not edited: treat it as a host failure by id, and name it in the code review. Add `tests/security/test_git_interpreter_binding_portable.py`, `tests/test_security_lint.py` and `tests/test_skills_install.py` to C1's guarding files. C1 is over the 40-file guard. Do not split the run: run the guarding files (`test_session_routines`, `test_session_kernel`, `test_session_failsafe`, `test_session_writes_contained`, `test_session_binding_gate_and_printing_hold`, `test_session_binding_untracked`, `test_skills_self_heal`, `test_first_session_report`, `test_status_vocabulary_advisory`, `test_next_session_local_note`, `tests/security/test_git_interpreter_binding_portable.py`, `tests/test_security_lint.py`, `tests/test_skills_install.py`, and the new file) and leave the broad selection to the arc's joined run.

**Hosts.** This Windows machine: all new tests, C1 (paths, README, `.gitignore`) and C2. Its Linux subsystem (development checks only): C1, C2 and C3 once for the POSIX branches, and C4 if Bandit is installed there; Bandit is not installed on the Windows machine (measured), so the real-Bandit case may wait for the joined run. Canonical runtime (`dev/rules/certifying-runs.md`, Python 3.13): nothing here certifies; the full run waits for the arc's joined run.

**Prose gates**, one file per call: `dev/tools/claim_check.py`, `dev/tools/link_check.py`, `tests/check_cairn.py`, `git diff --check`, on each changed `.md`.

**Issues, for the Maintainer.** Nobody closes or comments on any: #98 (parts 1, 2), #91 (part 2), #96 (partly), #101, #99 (part 6, answered).

**Not checked.** No code or test was run for this plan; Bandit's JSON output was not run; the message texts were not run in PowerShell; macOS; whether protected session tests pin a printed path. **Does any rule weaken or disappear?** No rule text is edited.

## Plan review -- Claude Sonnet 5.5 (`claude-sonnet-5-5`, usual reviewer) -- 2026-11-20

```
Reviewed commit: d4a90f7622d939c3d7327f3f5f23d7d52aa64e3e
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

The plan turns six adopter reports into small edits with exact texts. Most of it holds: the twelve path sites count correctly, every twin pair is byte-identical, the selector counts reproduce, and the C3 fixtures behave as the companion says on synthetic records. Three gaps would stall or mislead a low-tier implementer.

**Foundations**

1. **Should this happen as framed?** Yes. #96's accepted wording is delivered (the `unsupported_record` trigger goes); Claude stays UNKNOWN because its events are never proven -- `meter.py:3717`, `6624`.
2. **Best alternative.** Bandit's own `-ll`/`-ii` flags are simpler but hide below-threshold findings, which the proposal's S5 wants printed; keep the JSON route -- `run_security_audit.py:853`.
3. **What would show it wrong.** A 4,000-byte policy file of `[` crashes the audit with a traceback instead of exit 20 -- the new C4 case in block C.

**Does any rule weaken or disappear?** No.

**Findings**

1. **Blocking.** Three frozen files change, not two: the gate manifest also freezes `measurements.py` as `scripts/measurements.py`, contradicting item 6's own rule. Words: block A.
2. **Blocking.** C1's baseline rule cannot work for one test. `test_session_failsafe.py:356` expects a backslash path in the `interpreter:` line, so on Windows it fails before and after C1 with different text. The ten guarding files also omit the binding-reader and lint tests. Words: block B.
3. **Blocking.** D7's loader leaves exception classes open. Measured: `json.loads('[' * 4000)` raises `RecursionError`, not `ValueError`. Words: block C.
4. Non-blocking. The #96 question is not plain; say what stays UNKNOWN. Block D.
5. Non-blocking. The policy file is not hash-covered, which `python-security.md` says policy inputs are. Block E.
6. Non-blocking. "The same `exec` findings" omits the twelfth, `pulse.py` B314 (also allowed in `security_check.py:220`). Name it in the prose.
7. Non-blocking. Stubbed audit tests carry the "Declared exception (internal hook)" comment, as `test_security_stack.py` does. State whether the threshold suffix goes on DEGRADED statuses (this review suggests no). The C3 real-log check runs from a scratch folder outside the repository, printing integers and issue names only.

**Not covered.** No test, audit or Bandit run; Windows prints; macOS; the manifest's old-path keys beyond the three hashes; whether the Security pass accepts the threshold line missing from the default summary. Over target: three blocking findings.

**Elapsed**: about 45 minutes. **Tokens**: unknown.

### Exact words for the plan review above

**A (replace the Staleness sentence "The gate manifest freezes two files changed here; the verifier will show two HOLDs for the Maintainer.").** "The gate manifest freezes three files changed here: `conflict.py`, `run_security_audit.py` and `measurements.py` (listed there as `scripts/measurements.py`); the verifier will show three HOLDs. Reason for the third: one comment now names `dev/tools/`; no code changes. Not run." In item 6, after "Left: comments in frozen files not otherwise edited", add "(`measurements.py` is the one exception: the HOLD is taken because the comment misleads adopters)". Or move `measurements.py` to plan D and delete it from item 6, the Protected list, C5 and D8.

**B (add to Verification, after "a failure is a host failure only if both are on the first list.").** "One exception, by design: `test_session_failsafe.py::test_interpreter_resolved_from_local_env_and_reported` expects a backslash path, so on Windows it fails before C1 (the line shows `\x5c`) and after (it shows `/`), with different text. It is frozen and not edited: treat it as a host failure by id, and name it in the code review. Add `tests/security/test_git_interpreter_binding_portable.py`, `tests/test_security_lint.py` and `tests/test_skills_install.py` to C1's guarding files."

**C (add to D7 step 4).** "Catch `ValueError` and `RecursionError` around the parse. The repeated-key hook raises a private `_DuplicateKey(ValueError)`, caught first, giving 'a key is repeated'. Step 1 covers `FileNotFoundError` only; any other `OSError` from `lstat` gives 'it cannot be read'. Read with `f.read(4097)`, never `read_bytes()`. Add one permanent case: 4,000 `[` characters gives `AuditDegraded`."

**D (replace the Question paragraph).** "**Question for the Maintainer.** After C3 the Pulse still shows Claude usage as UNKNOWN and the goodnight report still has no Claude numbers, because the meter never ties a Claude record to this project: it does not trust the folder a log sits in. Should it? Yes counts Claude usage once the folder matches the project; no keeps today's strict refusal. Default: no change now; decide in the tightening or v0.10."

**E (add to the `python-security.md` text in D7).** "Unlike the gate scripts, this file is not hash-checked by the lock; the printed threshold is how a change is seen."

## Security Review -- Claude Opus 5.5 (`claude-opus-5-5`, Security reviewer) -- 2026-11-20

```
Reviewed commit: b982d307709054f75235703f551d51661deb8b43
```

**Obligation**: Internal Security Review
**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

The plan adds one adopter-set threshold, narrows one completeness flag and changes how paths print, keeping every default as strict as today. Mostly it holds: a bad, empty, unreadable or linked policy file stops the audit (exit 20); no listed value switches Bandit off.

**Foundations**

1. **Should this happen as framed?** Yes; the threshold was accepted with "printed on every audit result" -- the proposal's Security Review, finding 3, and its response.
2. **Best alternative.** Bandit's `-l`/`-i` flags would hide below-threshold findings; keep the printed JSON route -- `run_security_audit.py:860`.
3. **What would show it wrong.** Block S3's nested-usage fixture leaving `issues == []` after C3.

**Findings**

1. **Blocking.** Exceptions other than `AuditDegraded` escape the loader and the classifier (`main` catches only that, `run_security_audit.py:1856`); a list-valued level fails a set lookup with `TypeError`. D7 also names `_REPO_ROOT` where the loader takes `repo_root`. Block S1; it governs over the usual review's block C.
2. **Blocking.** The threshold line is S5's only control and no test pins it. Usual review's open point: the default summary may omit the suffix if the line is pinned and the module page says what no suffix means. Block S2.
3. **Blocking.** C3 checks `usage` at two places only, so a new record type with usage deeper is skipped silently where today it is flagged; the plan's "a usage-bearing record of an unknown type still does" is then false. Block S3.
4. Non-blocking. C1(c) strips leading spaces, as the existing test does (`session.py:1433`); Git keeps them. No write path is opened.
5. Non-blocking. S1 claims a size cap on every reader; the `.gitignore` gets none new. Say so.

Agreed with usual findings 1, 2 and 4 to 7, including no suffix on DEGRADED. Checked without findings: `encode_display_path` still ends in `encode_display` (`session.py:196`); the Windows execute-bit skip changes a refusal label only (`conflict.py:643`); no new record is counted (`meter.py:6606`). #96's outcome is delivered once S3 is closed.

**Not covered.** No code, test or Bandit run; linked `dev` or `dev/.cairn` parents; whether Bandit reads a `.bandit` file inside `python_package` (an unprinted knob older than this plan); macOS.

**Elapsed**: about 35 minutes. **Tokens**: unknown.

### Exact words for the Security Review above

**S1 (add to D7, after step 6).** "Paths: the file is `repo_root / "dev" / ".cairn" / "python-security.json"`, `repo_root` being the argument (`main` passes `_REPO_ROOT`). Levels are accepted only if `isinstance(value, str) and value in ("low", "medium", "high")`. Backstop: any exception other than `AuditDegraded` raised inside `load_bandit_policy` becomes `AuditDegraded` with the reason 'it cannot be read'; any exception inside step 5's parse and ranking gives `bandit:unparseable`, DEGRADED. A severity or confidence that is not a string ranks 99. Add two permanent cases: `{"schema": ..., "min_severity": ["high"]}` gives `AuditDegraded`; output `"[" * 4000` gives `bandit:unparseable`."

**S2 (add to D7's permanent cases).** "Capture stdout: with no file, and with a file setting both minimums to `low`, the first `[bandit]` line is the matching step 2 text and the status has no suffix; with `medium`/`low` the first line names both minimums and every returned status ends with the suffix." Add to the `python-security.md` text: "A Bandit status in the summary with no `[threshold: ...]` suffix means the default: any finding fails."

**S3 (replace D6's helper sentence).** "`_record_carries_usage(record)`: walk the record without recursion (a list used as a stack, over dict values and list items); return True if any dict has the key `usage`." Add the fixture `{"type": "future-record-type", "data": {"message": {"message": {"usage": {}}}}}`, expecting `unsupported_record`. In the developmental check: if `unsupported_record` still appears after C3, stop and report the record-type counts to the Maintainer; do not narrow the walk.

## Plan response -- Claude Sonnet 5.5 (`claude-sonnet-5-5`, for the author) -- 2026-11-20

Both reviews said REVISE. Every blocking finding is applied with its reviewer's words; where the two touch the same point, the Security Review governs. Status is now `ready-to-implement`.

**Usual review**

1. Blocking (A): accepted, taking A's words and keeping the `measurements.py` edit in this plan (not moving it to plan D). Staleness sentence replaced; the exception is added in Scope item 6.
2. Blocking (B): accepted; added to Verification after the host-failure sentence, and the three files are in the guarding list.
3. Blocking (C): replaced by S1, not applied. Not carried over from C: `_DuplicateKey`, the `f.read(4097)` rule, and the `lstat` `OSError` wording; S1's backstop covers the exception classes.
4. Non-blocking (D): applied; the Question paragraph is replaced.
5. Non-blocking (E): applied; added to the `python-security.md` text in Detail D7.
6. Non-blocking, twelfth finding: named in Scope item 4 and in the D7 module-page text.
7. Non-blocking: declared-exception comment added to D7's test cases; no suffix on DEGRADED statuses (C4 and D7 step 8); the real-log check runs from a scratch folder, printing integers and issue names (D6).

**Security Review**

1. Blocking (S1): accepted, in Detail D7 after step 6.
2. Blocking (S2): accepted, at the end of D7's permanent cases and the module-page text.
3. Blocking (S3): accepted; D6's helper sentence is replaced, the fixture and the stop rule added.
4. Non-blocking (leading spaces): no change asked.
5. Non-blocking (size cap): the Security answer S1 now says only the policy file gets a size cap.

**Consistency changes**

- Protected list: `measurements.py` now has its own "(frozen, HOLD)" line.
- Detail D7 "Policy file": `_REPO_ROOT` became `repo_root` (S1 finding 1).
- C3 acceptance: the usage test now reads "any dict anywhere in the record" (S3 made the old wording false).
- C4 acceptance and D7 step 8: DEGRADED statuses carry no suffix.
- Module-page word target: "about 120" became "about 165" words.
- S2's "every returned status ends with the suffix" is read as the non-DEGRADED statuses.

**Left for the code review**: nothing. Could not apply exactly: nothing.

Not checked: no code or test run; no Bandit run; whether `pulse.py` B314 is the one the allow-list names, beyond the usual review's citation.

**Elapsed**: about 20 minutes. **Tokens**: unknown.
