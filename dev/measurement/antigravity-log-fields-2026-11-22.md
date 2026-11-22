# Antigravity logs: count-only follow-up on fields, transcript parity, and identity (2026-11-22, Mac)

This note adds follow-up measurements to [the initial look](antigravity-look-2026-11-22.md) and [the real-log check](antigravity-real-log-check-2026-11-22.md). It records only counts, approved key names from [custom session routines](../rules/custom_session_routines.md), environment checks, and the local sanitized `dev/measurement/meter.json` output on one Mac (Python 3.13.13). No raw log value, folder path, UUID, or unapproved key name appears here.

## Answer

**All 46 `transcript.jsonl` / `transcript_full.jsonl` pairs match identically on token records, newer Antigravity replies carry a top-level `model` field ignored today, every token record carries an unapproved cache-token count (~92.6% of total tokens), and Antigravity's folder UUID matches `ANTIGRAVITY_CONVERSATION_ID` rather than `ANTIGRAVITY_TRAJECTORY_ID`.**

## Folder and transcript parity

| Measure | Count |
|---|---|
| Folders under `brain/` | 48 (47 UUID-named, 1 non-UUID) |
| UUID folders with `.system_generated/logs/` and `transcript.jsonl` | 47 |
| UUID folders also holding `transcript_full.jsonl` | 46 (1 has `transcript.jsonl` only; 0 have `transcript_full.jsonl` only; 0 other `*.jsonl` files) |
| Exact `(created_at, input_tokens, output_tokens)` multiset parity across pairs | 46 of 46 match (0 mismatches) |
| Token records (`transcript.jsonl` vs `transcript_full.jsonl`, live snapshots) | 6,162 vs 6,162 at 17:12 EST (`30,326` vs `18,754` JSONL lines, 0 malformed); 6,172 vs 6,172 at 17:20 EST |

`dev/tools/meter.py` currently reads every `*.jsonl` directly under `logs/`, reading duplicate token records from `transcript_full.jsonl` and exposing lines to the 8 MiB limit on untruncated payloads.

## Live `model` and cache-token fields

- **Approved `model` key:** At the 17:20 EST scan, `37` of `38` token records dated `2026-11-22` (1 conversation) carry a non-empty top-level `model` string; `0` of `6,134` earlier records carry one. In a count-only format check on 30 `model` values at 17:13 EST, all `30` pass `meter._safe_alias` (19 characters, lowercase and hyphens only, 1 distinct value), and `0` of `30` match `_RATIO_INDEX["models"]` in [`dev/tools/meter.py`](../tools/meter.py) by exact or lowercased lookup because `_RATIO_INDEX` hardcodes bare model names without variant suffixes. [`dev/tools/meter.py`](../tools/meter.py) currently leaves `model` and `effective_model` unset (`None`) for all Antigravity events.
- **Unapproved cache-token key (counted, not named):** Every token record (`6,172` of `6,172` at 17:20 EST) carries 4 top-level integer keys: `input_tokens`, `output_tokens`, one other unapproved integer key, and one unapproved non-negative integer key matching a case-insensitive `cache` + `token` substring check (`> 0` in `5,926` of `6,172` records, `96.0%`; `> input_tokens` in `5,884` of `6,172`, `95.3%`). Across all `6,172` records: `input_tokens = 65,476,772`, `output_tokens = 4,066,631`, and that cache-token key sums to `867,668,476` (`13.3x` `input_tokens`; `92.6%` of the three sums combined).

## Session identity and current sanitized meter state

- **Environment variables (checked in shell, not in logs):** Both `ANTIGRAVITY_CONVERSATION_ID` and `ANTIGRAVITY_TRAJECTORY_ID` are set and differ (`conv_eq_traj = false`). `ANTIGRAVITY_CONVERSATION_ID` names an existing `brain/<uuid>` folder; `ANTIGRAVITY_TRAJECTORY_ID` does not. [`dev/tools/_intent/identity.py`](../tools/_intent/identity.py) (line 47) reads only `ANTIGRAVITY_TRAJECTORY_ID`, explaining the non-matching `antigravity-<8 hex>` tags noted in [the Antigravity reader plan](../plans/archive/2026-11-22-antigravity-reader.md).
- **Sanitized `dev/measurement/meter.json` (`cairn-meter-project/2`):** Shows 3 `cairn` rows for `2026-11-22` (`events` across the 3 rows: `1` Antigravity reply with `model=null`, `fresh_input=6,601`, `output=4,260`, `cache_read=null`, `cache_write=null`, `weighted=null`; `98` `claude-opus-5-5` replies with weighted total `5,708,158.6`; `1,295` `claude-sonnet-5-5` replies with weighted total `61,989,689.6`), coverage reasons `antigravity_project_inferred`, `antigravity_unattributed`, and `global_completeness_unknown`, and no agent-tier field or `by_tier` summary.
- **Template neutrality gate:** Running `tests/quality_gate.py --sub neutrality --report` reported 8 failures: 7 in [`templates/core/dev/measurement/README.md`](../../templates/core/dev/measurement/README.md) (lines 45–59) naming models/makers from `meter.py`'s hardcoded `_RATIO_INDEX`, and 1 pre-existing hit in [`templates/skills/session-start/SKILL.md`](../../templates/skills/session-start/SKILL.md) (line 27).

## Not checked

- Exact key name of the unapproved cache-token field (withheld under [custom session routines](../rules/custom_session_routines.md) pending Maintainer authorization).
- Hand-labelled conversation attribution sample and multi-day/Windows Antigravity runs.
- Sub-agent conversation linkage beyond noting 1 conversation in `transcript.jsonl` holding 6 `invoke_subagent` calls.
