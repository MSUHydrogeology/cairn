# Detail for plan C of the defect arc: exact conditions, texts and fixtures

This file is part of `dev/plans/archive/2026-11-20-defect-arc-c-first-session-and-tools.md`. It exists because the plan must leave no design to a low-tier implementer, and the exact texts would push the plan far over its word target. Line numbers are at `02f92d37`; find each site by the function name and text given, not by the number alone. Where a shipped file has a twin, edit both and compare with `cmp` afterwards.

## D1. README (C1)

File pair: `templates/skills/_lib/session.py` and `dev/tools/session.py` (byte copies; edit one, copy it over the other).

In `_in_flight_items`, the condition `if path.name != "_template.md":` becomes `if path.name != "_template.md" and path.name.lower() != "readme.md":`. Nothing else changes. `_in_flight` and `_in_flight_status_advisory` both read this walk, so they stay in step.

## D2. Forward slashes (C1)

Add `encode_display_path(value)` directly after `encode_display`. Behaviour: `text = str(value)`; if `os.sep == "\\"`, `text = text.replace("\\", "/")`; return `encode_display(text)`. Docstring, in one sentence: Windows folders are separated by a backslash that the encoder would print as `\x5c`, which cannot be pasted back; on POSIX a backslash in a name stays escaped.

Replace `encode_display(str(X))` or `encode_display(X)` with `encode_display_path(X)` at exactly these twelve sites, and nowhere else:

1. `_assert_within`: the two path values in the "refusing to write outside" message (`base`, `path`).
2. `_assert_not_linked`: `dst` in the `_OUTSIDE_REFUSAL` line (the first one, with `str(dst)`).
3. `_resolve_interpreter`: `shown_cfg` (`str(cfg)`), `shown_interp` (`str(interp)`), and `sys.executable` in the "no longer exists" warning.
4. `_assert_fanout_contained`: `ancestor` and `final`.
5. `_heal_skill_symlink`: `dst` in the "exists as a non-symlink" warning.
6. `_heal_skill_copy`: `dst` in the "copy-fallback divergence" warning.
7. `cmd_session_start`: `interpreter` in the `interpreter:` line.
8. `_reclaim_or_refuse` (the handoff lock): `self.path`.

Unchanged: every `encode_display(str(exc))`, `encode_display(name)`, the vendor-table `path` in the "unsafe vendor path" warning (a POSIX string from a table), `rel.as_posix()` uses, `_encode_child_output` and `_safe_field`. The protected printing tests pin `encode_display` and `_safe_field`, which this change does not touch.

## D3. `.gitignore` check (C1)

In `_seed_skill_gitignore`, keep the existing literal test (`norm in {...}`) and its early return exactly. Directly after it, add: `if _gitignore_covers(text, entry): return`.

`_gitignore_covers(text, entry) -> bool`, new, no Git call:
1. `lines = [ln.strip() for ln in text.splitlines()]`.
2. If any line starts with `!`, return False. A later negation may re-include the folder; the old behaviour (add the line) is the safe one.
3. `parts = entry.strip("/").split("/")` (for `.claude/skills/`: `[".claude", "skills"]`).
4. `covers` is a set: for each prefix `p` (the first i parts joined by `/`, i from 1 to the full length) add `p`; for each proper prefix (i less than the full length) also add `p + "/*"` and `p + "/**"`.
5. For each line that is non-empty and does not start with `#`: `cand = line.lstrip("/").rstrip("/")`; if `cand in covers`, return True.
6. Return False. Wildcard rules such as `.c*/` are not recognized and fall through to today's behaviour.

The reason it is text and not `git check-ignore`: that form is not allowed by the pinned Git helper, which stays unchanged.

## D4. Handoff refusal text (C1)

In `_do_full_handoff`, the `LifecycleError` raised when `_designation_marker_present` is false becomes this one string (plain `"..."` pieces, no f-string, so `$env` and braces need no escaping):

> refusing the full handoff: no maintainer-designation marker. To run it as the designated single owner, set CAIRN_HANDOFF_OWNER=1 for one command. In bash or zsh: CAIRN_HANDOFF_OWNER=1 python dev/tools/session.py session-end --handoff. In PowerShell: $env:CAIRN_HANDOFF_OWNER = '1'; python dev/tools/session.py session-end --handoff; Remove-Item Env:CAIRN_HANDOFF_OWNER. Or create the file dev/.cairn/handoff-owner. This is an anti-accidental-run gate, not an authorization control -- run with --dry-run to preview the manifest first.

Two existing protected tests assert only the phrase "no maintainer-designation marker"; keep it. No permanent test pins the new wording.

## D5. Execute bit (C2)

In `_classify_existing_precommit` (both `conflict.py` files), `if not (hook_file.stat().st_mode & 0o111):` becomes `if os.name != "nt" and not (hook_file.stat().st_mode & 0o111):`. `os` is already imported there. The Windows result for a plain shell hook is `foreign` (refused, file unchanged), as for any other existing hook. `hooks.py` is not changed: its post-commit test uses `os.access`, and its `chmod` calls are harmless on Windows.

## D6. Usage-free records (C3)

Both `meter.py` copies. Add, next to the other small helpers before `read_records`, a function with no vendor word in its name (so the neutrality lint needs no marker):

`_record_carries_usage(record)`: walk the record without recursion (a list used as a stack, over dict values and list items); return True if any dict has the key `usage`.

In the Claude branch (the `if tool == "claude":` block that begins `if kind != "assistant":`), change the inner test to: `if kind not in {"user", "system", "progress", "file-history-snapshot"} and _record_carries_usage(record):` then `issues.add("unsupported_record")`; the `continue` stays. The Codex branch and its `unsupported_record` are not touched.

Fixtures, written by hand in `tests/test_meter_usage_free_records.py`, one assistant record shaped like the one in `tests/integration/test_meter.py::claude()` (copy its key names, not its values) plus:
- Usage-free, parametrized: `{"type": "queue-operation"}`, `{"type": "attachment"}`, `{"type": "api-request"}`, `{"type": "last-prompt"}`, `{"type": "future-record-type"}`, and one with no `type` key at all. Expect `issues == []` and one event.
- `{"type": "future-record-type", "message": {"usage": {}}}` and `{"type": "future-record-type", "usage": {}}`: expect `"unsupported_record"` in `issues`.
- `{"type": "future-record-type", "data": {"message": {"message": {"usage": {}}}}}`: expect `"unsupported_record"`.
- An assistant record whose `message.usage.output_tokens` is `-1`: expect `"invalid_record"` and an event whose kinds are all unknown.
- The four existing names: expect `issues == []`.

Developmental check on real logs (this machine, counts only, script deleted afterwards; run it from a scratch folder outside the repository and print only integers and issue names): load `dev/tools/meter.py`, feed the lines of the current project log to `read_records("claude", lines)`, print only `len(events)` and `issues`. Starting commit: `unsupported_record` is listed. After C3: it is not, and `invalid_record` is listed only if some assistant usage fails to parse (the measurement before the plan: none). If `unsupported_record` still appears after C3, stop and report the record-type counts to the Maintainer; do not narrow the walk.

## D7. Audit threshold (C4)

File: `templates/modules/team-gated/run_security_audit.py` (no copy exists under `dev/tools`; Cairn does not install this module). Prose: `templates/modules/team-gated/python-security.md`, a new subsection "Setting a severity threshold" after "Exit contract".

**Policy file.** Path `repo_root / "dev" / ".cairn" / "python-security.json"`. Optional; absent means default. Adopter-owned: it is not in the apparatus set, so the integrity preflight does not hash it. Shape:

```
{"schema": "cairn-python-security-policy/1", "min_severity": "medium", "min_confidence": "low"}
```

`schema` is required and must equal that string. `min_severity` and `min_confidence` are optional, each exactly `low`, `medium` or `high` (lower case), each default `low`. Any other key is refused.

**Loader** `load_bandit_policy(repo_root) -> BanditPolicy` (a NamedTuple of `min_severity`, `min_confidence`, `from_file: bool`). Steps, each failure raising `AuditDegraded` with the text below:
1. Path missing (`FileNotFoundError` from `lstat`): return the default policy, `from_file` False.
2. `is_symlink()` or not `is_file()`: "it is not a regular file (a link, folder or special file)".
3. `stat().st_size` above 4096, or the bytes read above 4096: "it is larger than 4096 bytes".
4. Read error: "it cannot be read". Not UTF-8 or not JSON: "it is not valid UTF-8 JSON". Parse with `object_pairs_hook` that raises on a repeated key: "a key is repeated". Top level not an object: "it is not a JSON object".
5. `schema` missing or wrong: "the schema value must be cairn-python-security-policy/1".
6. Unknown key: "an unknown key was found: " plus the key run through `escape_controls` and cut to 40 characters. A level that is not one of the three words: "min_severity must be one of low, medium, high" (or `min_confidence`).

Paths: the file is `repo_root / "dev" / ".cairn" / "python-security.json"`, `repo_root` being the argument (`main` passes `_REPO_ROOT`). Levels are accepted only if `isinstance(value, str) and value in ("low", "medium", "high")`. Backstop: any exception other than `AuditDegraded` raised inside `load_bandit_policy` becomes `AuditDegraded` with the reason 'it cannot be read'; any exception inside step 5's parse and ranking gives `bandit:unparseable`, DEGRADED. A severity or confidence that is not a string ranks 99. Add two permanent cases: `{"schema": ..., "min_severity": ["high"]}` gives `AuditDegraded`; output `"[" * 4000` gives `bandit:unparseable`.

Every message is the prefix `the python-security policy file dev/.cairn/python-security.json cannot be used: `, the reason, then `. Fix the file, or delete it to restore the default (any finding fails). The audit will not pick a threshold for you.` No raw value other than the escaped, cut key name is echoed.

**Pass flow** in `run_bandit_pass` (rename today's body `_run_bandit_default`, unchanged; keep the one public signature):
1. `policy = load_bandit_policy(repo_root)`.
2. Print first (stdout). No file: `[bandit] threshold in force: any finding fails (default; no dev/.cairn/python-security.json).` With a file (even one that sets both minimums to `low`): `[bandit] threshold in force: severity at least <S> and confidence at least <C>, set in dev/.cairn/python-security.json. A finding below it is printed but does not fail the audit.`
3. If both minimums are `low`: return `_run_bandit_default(pkg, repo_root)` unchanged (a file that sets the defaults changes nothing).
4. Otherwise do the same Bandit-installed check, then run argv `[sys.executable, "-I", "-m", "bandit", "-r", "-f", "json", *_safe_target_args([pkg])]` (no `-q`; stdout is then only the JSON, the log lines go to stderr) through `_run_tool(label="bandit")`. A status other than `ran`, or `tool-absent`, maps as today (DEGRADED).
5. Classify: code not 0 or 1 gives `bandit:error`, DEGRADED. `json.loads(run.stdout)`; not an object with a list `results` of objects: `bandit:unparseable`, DEGRADED. Rank `LOW`=1, `MEDIUM`=2, `HIGH`=3; a missing or other value ranks 99 so it fails. `failing` = findings whose `issue_severity` rank and `issue_confidence` rank are both at least the minimums. Code 0 with any finding, or code 1 with none: `bandit:inconsistent`, DEGRADED.
6. Print `[bandit] <N> finding(s) at or above the threshold (these fail the audit); <M> below it (printed above; they do not fail the audit).`
7. No findings: `bandit:clean`, tier 0. Any failing: `bandit:findings`, tier 10. Only below: `bandit:clean-below-threshold`, tier 0.
8. Every status from this path (non-default only) that is not DEGRADED ends with ` [threshold: severity>=<S>, confidence>=<C>]`; DEGRADED statuses carry no suffix.

Permanent test cases (stub `_run_tool` with hand-written JSON; the stub records the argv): no file gives no `json` in argv and today's verdict; medium/low with one LOW and one MEDIUM fails with count 1 and 1; high/low with LOW and MEDIUM passes below-threshold and the summary status carries the suffix; medium/high with MEDIUM severity and LOW confidence passes, with HIGH confidence fails; `UNDEFINED` severity fails; each refusal of step 2 to 6 (symlink skipped where links cannot be made) gives `AuditDegraded`; unparseable output, code 0 with a finding, code 1 with none, and code 2 are DEGRADED. Real Bandit, skipped when `_HAS_BANDIT` is false: a one-file package with an `assert`, passes under `high` and fails by default. Stubbed tests carry the "Declared exception (internal hook)" comment, as `tests/test_security_stack.py` does. Capture stdout: with no file, and with a file setting both minimums to `low`, the first `[bandit]` line is the matching step 2 text and the status has no suffix; with `medium`/`low` the first line names both minimums and every returned status ends with the suffix.

**`python-security.md` text** (about 165 words, plain): where the file lives and its three keys; that a finding fails when severity and confidence are both at or above the minimums; that the default is unchanged; that the audit prints the threshold at the top of the Bandit section and in the summary, prints every finding, and counts those below; that a bad file stops the audit with exit 20; that the audit scans only `python_package`, so Cairn's own tools under `dev/tools` are not re-scanned (they are hash-checked), and that a whole-tree scan of your own will show Cairn's deliberate `exec` of verified bytes, and one XML parse in `pulse.py` (B314), which Cairn allows in its own release gate. Unlike the gate scripts, this file is not hash-checked by the lock; the printed threshold is how a change is seen. A Bandit status in the summary with no `[threshold: ...]` suffix means the default: any finding fails.

## D8. Comments (C1, C2, C5)

Comment text only; `ast.dump(ast.parse(...))` of each changed file must be equal before and after.
- `session.py`, both copies, line 127: the pre-0.8 test folder in front of `test_session_kernel.py` becomes `tests/`. (A docstring near `_safe_field` names the same file; it stays, because a docstring is not a comment.)
- `intent.py`, both copies, line 56: `bootstrap/scaffold.py's launcher` becomes `install/scaffold.py's launcher`.
- `templates/modules/default-on/measurements.py`, line 19: `<cairn>/scripts/` becomes `<cairn>/dev/tools/`.

## D9. Order inside each chunk

Write the failing permanent test first and run it at the starting commit to see the reason; then the fix; then the selected files, compared with the first list. C1 is cut into the five sub-steps D1 to D4 and D8, each checked alone, in that order.
