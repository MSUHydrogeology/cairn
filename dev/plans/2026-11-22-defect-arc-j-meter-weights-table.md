# Plan: Defect arc J, the meter's table of token weights

**Source proposal**: dev/proposals/archive/2026-11-20-claude-v09-defect-arc.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-22
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/development-environment.md
**In brief**: The usage meter's table of token weights will cover the models now in use, will keep a usage history readable when the table changes, and will weight Codex replies by the model they selected.

## Build summary

Counted on the Windows Server machine (counts and model ids only): Cairn's Claude logs hold 6,913 replies from four models, `claude-fable-5-2` 1,975, `claude-sonnet-5-5` 3,273, `claude-opus-5-5` 835 and `claude-haiku-5-5` 830. Only Opus 5.5 has a row in `_RATIO_INDEX`, so the others get counts and no weighted total. This plan adds rows for those models, the newest OpenAI and Gemini models and a second price level for long prompts. It also stops a table change from making the ledger unreadable, and weights a Codex reply by its turn's selected model. Totals are reference figures, never bills.

## Source proposal

The accepted defect arc takes in defects found since. This one is roadmap item (q), and the Maintainer asked for it on 2026-11-22: "Please fill in the table of weighting once you've done your research. On Gemini, use Neon for the mid, Argon for high, and Hydrogen for low."

## Scope

All in `dev/tools/meter.py` (then its shipped copy), a small part of `dev/tools/pulse.py` (and copy), tests, both measurement READMEs and `CHANGELOG.md`. No doctrine surface. No new script, option or file. The model mapping (done) and an Antigravity reader are not here.

**Read in the code, 2026-11-22.** (3) `_load_ledger` raises `ValueError` (ending as `ledger_invalid`) unless `ledger["ratio_version"] == RATIO_VERSION` and `ledger["ratio_index"] == _RATIO_INDEX`, and `_validate_aggregate_row` demands `reference_index == RATIO_VERSION`; so any table change refuses every ledger, and the README's only cure is to move the file aside. Nothing else reads the stored table. True. (5) The Codex reader sets `effective_model=None` with provenance `selected_context` (`_validate_event` forbids both together), and `_weighted_reference_tokens` reads only `effective_model`: a Codex reply gets no weighted total. True. One more fact: the reader keeps `cache_write` unknown when a log omits `cache_write_input_tokens` and records 0 when it is an explicit 0, so a Codex reply still has no total if its log omits the field. Whether real Codex logs carry it is not checked (no log was read).

**(a) The table.** `RATIO_VERSION = "cairn-api-token-index/2026-11-22"`, `as_of` `2026-11-22`, `profile` unchanged (still true). `sources` becomes the three pages below. Existing four rows stay. Each cell `a/b` is the weight `[a, b]`; a bare `n` is `[n, 1]`; a weight is US dollars per million tokens at the maker's public standard price (read 2026-11-22). Not checked: the OpenAI and Google keys are the makers' own model ids, not ids read from a real Codex or Antigravity log, and no Antigravity reader exists, so the Gemini rows wait for one. Argon's row is its standard price from 2026-12-01; its introductory price (2, 1/10, 10 until 2026-11-30) is not used, because the table excludes discounts.

Anthropic, `https://platform.claude.com/docs/en/about-claude/pricing`:

| key | fresh_input | cache_read | output | cache_write_5m | cache_write_1h |
|---|---|---|---|---|---|
| `claude-fable-5-2` | 8 | 1/5 | 40 | 10 | 16 |
| `claude-sonnet-5-5` | 2 | 1/10 | 10 | 5/2 | 4 |
| `claude-haiku-5-5` | 1/10 | 1/100 | 1/2 | 1/8 | 1/5 |
| same, `long_prompt` over 100000 | 1/2 | 1/20 | 5/2 | 5/8 | 1 |

OpenAI, `https://developers.openai.com/api/docs/pricing`; `cache_write_5m` and `cache_write_1h` are `None`, as in the Codex row now:

| key | fresh_input | cache_read | output | `long_prompt` over 272000: fresh, read, output |
|---|---|---|---|---|
| `gpt-6.2-sol`, `gpt-6.1-sol` | 2 | 1/10 | 10 | 4, 1/5, 15 |
| `gpt-6-sol` | 2 | 1/5 | 10 | 4, 2/5, 15 |
| `gpt-6.1-terra` | 1 | 1/20 | 5 | 2, 1/10, 15/2 |
| `gpt-6-luna` | 1/10 | 1/100 | 1/2 | 1/5, 1/50, 3/4 |

Google, `https://aistudio.google.com/docs/pricing`, paid tier; no write weights (`None`), no second level:

| key | fresh_input | cache_read | output |
|---|---|---|---|
| `gemini-4-argon` | 4 | 1/5 | 20 |
| `gemini-4-neon` | 3 | 3/20 | 15 |
| `gemini-4-hydrogen` | 3/2 | 3/40 | 15/2 |

**(b) Two price levels.** A row may carry `"long_prompt": {"over_tokens": n, <the five weight keys>}`. Anthropic's page counts cache reads and writes in the prompt, so the prompt is the sum of three counts:

```python
level = weights
long_level = weights.get("long_prompt")
if long_level is not None:
    counts = (kinds["fresh_input"], kinds["cache_read"], kinds["cache_write"])
    if None in counts:
        return {name: None for name in (*_EVENT_KIND_NAMES, "total")}
    if sum(counts) > long_level["over_tokens"]:
        level = long_level
```

then the loop and the cache-write step read `level`. My reading of "the total is unknown": with a second level and an unknown count the weights cannot be chosen, so every figure is unknown.

**(e) Codex replies.** At the top of `_weighted_reference_tokens`:

```python
model = event["effective_model"]
if model is None and event["model_provenance"] == "selected_context":
    model = event["model"]
```

The reader and `_validate_event` stay as they are, so the summary still says the name came from `selected_context`. The first test below passes an abstract event with no `model_provenance` key but an `effective_model`; the `and` is not reached for it. This is Strategy's choice, not the Maintainer's instruction; a reviewer may disagree. Reason: a weighted total is a reference figure, never a bill; a turn's selected model is ordinarily the model that answers it; without this no Codex work is ever weighted. Cost: a turn whose answering model differs is priced as the selected one.

**(c) A ledger outlives a table change.** The label form lives once, in `pulse.py` (the meter already loads it as `_PULSE`): `RATIO_VERSION_FORM = re.compile(r"cairn-api-token-index/[0-9]{4}-[0-9]{2}-[0-9]{2}")`, used with `fullmatch`. In `_load_ledger` the two equality tests become

```python
or not isinstance(ledger["ratio_version"], str)
or not _PULSE.RATIO_VERSION_FORM.fullmatch(ledger["ratio_version"])
or not isinstance(ledger["ratio_index"], dict)
```

and, after the shape checks pass, `ledger["ratio_version"] = RATIO_VERSION` and `ledger["ratio_index"] = _ratio_index_copy()`. `_validate_aggregate_row` accepts any `reference_index` of that form (a string, `fullmatch`). `_add_rows` keeps the label when the two rows agree, else uses `RATIO_VERSION`. Retained replies already take the current table: `_new_ledger` rebuilds every non-folded aggregate from the held replies with `_recompute_aggregates`, which calls `_weighted_reference_tokens` each refresh. A folded day keeps its figures.

*For Security Review.* The old equality made a ledger valid only for the table that wrote it; no code reads the stored table or the stored label back, and the ledger is the user's own file with the account's own access. Kept: every other shape and bounds check (field sets, counters, decimal-string figures, the 64 MiB size cap), and the label must still match the exact form. A folded day keeps the weighting of its day, and the README says so. A label or table that is edited by hand can change only a figure that is labelled a reference figure.

**(d) The pulse.** `_parse_meter_aggregate` replaces `value["ratio_version"] != "cairn-api-token-index/2026-11-06"` with `not isinstance(value["ratio_version"], str) or not RATIO_VERSION_FORM.fullmatch(value["ratio_version"])`. It never reads the weights.

**Reuse.** Searched the repository (not archives or scratch) for `cairn-api-token-index`, `ratio_version`, `RATIO_VERSION`, `_RATIO_INDEX`, `ratio_index`: only `meter.py`, `pulse.py`, their two shipped copies and two test files hold them. One mechanism (b) serves Haiku 5.5 and the OpenAI rows; one pattern serves meter and pulse.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Change T1's two tests and the pin edits; run them (they fail); then (a), (b), (e) | none | table, two-level weights, Codex weighting |
| C2 | Add T2 and T3 and the two refusal lines; run (they fail); then (c), (d) | C1 | a ledger that survives a table change, an accepting pulse |
| C3 | Shipped copies, both READMEs, changelog; run the named tests once | C2; one code review at the end | the finished change |

## Acceptance criteria

**C1.** Weighted totals are exactly these (each worked from the tables; read from the code, not measured until the build runs them). Fable reply, fresh 10, cache read 8, 1-hour write 2, output 4: `80`, `1.6`, write `32`, `160`, total `273.6`. Haiku 5.5, same counts with a 5-minute write: prompt 20, so `1`, `0.08`, `0.25`, `2`, total `3.33`. Haiku 5.5 with fresh 100000, read 8, write 2, output 4: prompt 100010, over the limit, so `50000`, `0.4`, `1.25`, `10`, total `50011.65`. With fresh 99990 the prompt is exactly 100000, which is not over: `9999`, `0.08`, `0.25`, `2`, total `10001.33`. Codex reply, selected `gpt-6.2-sol`, the fixture's counts (fresh 12, read 8, write 0, output 4): `24`, `0.8`, `0`, `40`, total `64.8`; with the write field deleted: those figures but write and total `None`. A model with no row still gives all `None`.

**C2.** A ledger written under the previous table loads. The test starts a Claude home as `test_folding_changes_no_aggregate_sum` does (CLOCK, `claude_home_started`, `grow`, `at_clock` LATER), with replies in the approved project: one `claude-sonnet-4-6` reply on 2026-11-05 (fresh 10, read 8, write 0, output 4), which folds to a daily row with total `92.4`, and one recent `claude-sonnet-5-5` reply with the same counts, which stays held. After the first refresh the test rewrites `ledger.json`: `ratio_version` to `cairn-api-token-index/2026-11-06`, `ratio_index` to `{"version": "cairn-api-token-index/2026-11-06", "models": {}}`, the daily row's `reference_index` to the same, and the held reply's aggregate figures to `None`. A second refresh then answers `written` (the code's word for a good refresh), the daily row's counts, figures and old label are unchanged, `ledger_of(home)` carries `meter.RATIO_VERSION` and `meter._RATIO_INDEX`, and the held reply's aggregate and the project's `meter.json` row both show total `60.8`. T3: the pulse accepts a summary with `cairn-api-token-index/2027-01-15` and refuses `cairn-api-token-index/latest`. Two lines in `INVALID_LEDGER_EDITS` (`ratio_version` set to `"today"`; a daily row with `reference_index="today"`) stay refused as `ledger_invalid`: the planted bad input for Security Review. They are two lines in an existing parametrized test; Strategy may drop them.

**C3.** `cmp` of each shipped copy prints nothing; both READMEs and the changelog carry the text below; `link_check`, `claim_check`, `check_cairn` and `git diff --check` pass on each changed document.

Tests changed or added, by node id in `tests/integration/test_meter.py` unless marked:

- T1a `test_reference_index_uses_source_reported_cache_ttl_and_keeps_unknown_partial`: add the Fable and the three Haiku 5.5 cases.
- T1b `test_selected_codex_context_and_missing_write_do_not_make_a_weighted_total`, renamed `test_selected_codex_model_is_weighted_and_a_missing_write_is_not`: the expectations above; the abstract-event part stays.
- T2 (new) `test_a_ledger_written_under_an_older_table_loads_and_is_weighted_by_the_current_one`. It needs `priced_lines` to take `model` and `cwd` keywords, defaulting to today's.
- T3 `tests/integration/test_gauge.py::test_explicit_project_meter_aggregate_joins_pulse_without_private_reads` uses `2027-01-15` and gains the refusal.
- Pins changed, no new logic: `test_dated_reference_index_is_exact_and_not_actual_spend` (version `2026-11-22`, three sources, one spot check of the Haiku 5.5 `long_prompt`); `test_project_export_contains_only_sanitized_project_aggregates` and `test_copied_legacy_fork_reconciles_direct_usage_and_retains_lineage_proof` compare with `meter.RATIO_VERSION`. The test-gauge fixtures that carry `2026-11-06` stay: that version is well formed.

## Scope delta

**Scope delta**: preserved

## Verification

Changed promises: the weighted totals in each summary row and ledger, `ledger_invalid` for a table change (now gone), the pulse's `ratio_version` test. Run once on Windows with `C:\ProgramData\Anaconda3\python.exe -m pytest <node ids>`. Before the code change (C1 and C2 as above), T1a, T1b, T2, T3, the index-pin test and the two refusal lines must fail; after it, run those and the two comparing tests once: nine nodes in two files. Nothing else is run. `test_gauge.py` is unstable on this host (roadmap item (j)): if T3 fails for a reason that is the machine's, stop and report.

Not run: other hosts, the whole suite, any run on real logs (the build must not run the meter on real data). **Strategy's check, after the merge**, on the Windows Server machine with the old ledger left in place: a refresh answers `written`, and each Claude row of the summary carries weighted totals equal to an independent count priced by this table.

Also: `cp dev/tools/meter.py templates/skills/_lib/meter.py` and the same for `pulse.py` (`cmp` prints nothing). Cairn's lock by `install/scaffold.py upgrade --target . --finalize dev/tools/meter.py dev/tools/pulse.py dev/measurement/README.md`, alone in its commit, then `python install/verify_integrity.py --target .`. Under `## Unreleased` in `CHANGELOG.md`, two Minor lines, each citing this plan: "Fixed: The usage meter's table of token weights covers the models now in use (Claude Fable 5.2, Sonnet 5.5, Haiku 5.5, the newest OpenAI and Gemini models), prices a long prompt at its higher weights, and weights a Codex reply by its turn's selected model." and "Fixed: A new table of token weights no longer makes the usage ledger unreadable; days already folded keep their earlier weighting." Stale at the Maintainer's signing: the hash lines of `tests/integration/test_meter.py` and `tests/integration/test_gauge.py`, the renamed node in the gate manifest and the new T2 node. No second Windows ceremony.

**READMEs.** Neither says what a weighted total is. Add one paragraph in `dev/measurement/README.md` after "does not claim complete project history." and in `templates/core/dev/measurement/README.md` after "Full handoff retains its separate locked pre-prune refresh.":

"Each summary row also carries weighted totals: its tokens priced at the model maker's public list prices, in US dollars per million tokens, from the table in `tools/meter.py` dated 2026-11-22. A weighted total is a reference figure for comparing work, never a bill; the table leaves out taxes, subscriptions and introductory prices (Gemini 4 Argon's, which ends 2026-11-30, is not used). A request whose prompt is over a model's long-prompt limit (100,000 tokens for Claude Haiku 5.5, 272,000 for the OpenAI models listed) takes that model's higher weights. A model missing from the table, or a reply with an unknown count, gets counts and no weighted total. A Codex reply is weighted by the model its turn had selected. When the table changes, the ledger keeps working: replies still held one by one are weighted by the new table at the next refresh, and a day already folded keeps the weighting of its day."

In the first README, the sentence "An older ledger is refused with `ledger_old_schema`; move `~/.cairn/meter/ledger.json` aside to start a new one." stays true and is not changed.
