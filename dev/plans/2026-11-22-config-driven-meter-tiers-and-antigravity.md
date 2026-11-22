# Plan: Config-driven model weights, configurable agent tiers, and Antigravity fixes

**Source proposal**: dev/proposals/archive/2026-11-22-neon-config-driven-meter-tiers-and-antigravity.md
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-22
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/custom_session_routines.md, dev/rules/development-environment.md
**In brief**: Implement config-driven model weights and configurable ordered agent tiers (including `frontier`) in meter and pulse, migrate version-6 ledgers to version 7, and fix Antigravity's identity, transcript, model, and `cache_read_tokens` extraction for v0.8.1.

Proposed paths:
- `dev/.cairn/meter-models.json`

## Build summary

This plan executes all outcomes of the accepted [config-driven meter proposal](../proposals/archive/2026-11-22-neon-config-driven-meter-tiers-and-antigravity.md) in v0.8.1. `dev/tools/meter.py` and its shipped twin drop all hardcoded vendor pricing tables (`_RATIO_INDEX`) and load weights, configurable ordered capability tiers (with Cairn adding `frontier` above `high` for `Fable`, `Astra`, and `Carbon`), prefix/segment tier rules, and bounded Antigravity settings from an account-owned JSON config (`~/.cairn/meter-models.json`, reference copy at `dev/.cairn/meter-models.json`). Project exports advance to `cairn-meter-project/3` (`tier` per row plus ordered `by_tier`), ledgers migrate cleanly from `cairn-meter-ledger/6` to `/7`, `pulse.py` renders `tier` and `by_tier` across `/1`–`/3`, and Antigravity reads `transcript.jsonl` only, extracts `model` and `cache_read_tokens`, and prefers `ANTIGRAVITY_CONVERSATION_ID` in `_intent/identity.py`.

## Source proposal

Accepted at heavy tier on 2026-11-22 (`64baff49`): all outcomes ship in v0.8.1; `cache_read_tokens` (verified across `6,235 / 6,235` Antigravity token records) joins [`dev/rules/custom_session_routines.md`](../rules/custom_session_routines.md); `tiers` is config-driven (default `["high", "medium", "low"]`, with Cairn configuring `["frontier", "high", "medium", "low"]` and mapping `Fable`, `Astra`, `Carbon` to `frontier` in `dev/.cairn/meter-models.json` and [`dev/.cairn/model-selection-mapping.yml`](../.cairn/model-selection-mapping.yml) while leaving [`docs/methodology/roles.md`](../../docs/methodology/roles.md) 3-tier task floors untouched); and `~/.cairn/meter/ledger.json` moves aside after landing for clean W1 restart.

## Scope

Delivers in 4 chunks (`C1`–`C4`):
- **Changed code & twins:** [`dev/tools/meter.py`](../tools/meter.py), [`dev/tools/pulse.py`](../tools/pulse.py), [`dev/tools/_intent/identity.py`](../tools/_intent/identity.py), and byte-identical shipped twins under `templates/`.
- **Changed/added config & rules:** `dev/.cairn/meter-models.json` (new), [`dev/.cairn/model-selection-mapping.yml`](../.cairn/model-selection-mapping.yml) (`frontier` rows), [`dev/rules/custom_session_routines.md`](../rules/custom_session_routines.md) (`cache_read_tokens`), [`dev/measurement/README.md`](../measurement/README.md), [`templates/core/dev/measurement/README.md`](../../templates/core/dev/measurement/README.md) (staying vendor-neutral; `tests/quality_gate.py --sub neutrality` already 0 at `5aee2fba` and must stay exit 0), [`CHANGELOG.md`](../../CHANGELOG.md), and [`dev/.cairn/cairn-lock.yml`](../.cairn/cairn-lock.yml).
- **Out of scope:** Scaffold installer (`install/`), `docs/methodology/roles.md`, v0.9 [cost-per-plan](../proposals/2026-11-22-claude-cost-per-plan.md) plan-step rows, and preserving Antigravity attribution changes (`d42f7c8e`, `299de58f`) intact.
- **Reuse:** Reuses `_safe_alias`, `_windows_component`, `_counter`, `_is_link`, `_unique_object`, `_reject_constant`, `Fraction`/`Decimal` arithmetic, and `pulse._PULSE_LABEL` regex patterns (searched `dev/tools/meter.py` and `dev/tools/pulse.py` directly).
- **Documentation / doctrine surface:** No governing doc touched; deliberation edits in `dev/rules/custom_session_routines.md`, `dev/.cairn/model-selection-mapping.yml`, `dev/.cairn/meter-models.json`; descriptive edits in both measurement READMEs and `CHANGELOG.md`; lockfile updated via `--finalize`.

## Sequence

Work runs in a clean isolated Git worktree off `0.9-dev`; twin copies match via `cmp` before final verification. No chunk requires a Maintainer fence (post-merge `~/.cairn/` install and ledger backup follow Decision #5).

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | External model config (`cairn-meter-models/1`), weights/tier engine, v6->v7 migration | Plan ready | `meter.py` config loader/validator/tier & weight resolver, v6->v7 migration, `dev/.cairn/meter-models.json`, `dev/.cairn/model-selection-mapping.yml` |
| C2 | Export `cairn-meter-project/3`, `by_tier` rollup, `pulse.py` `/3` validation & rendering | C1 | `_project_export` `/3` + `by_tier` in `meter.py`; `models_config_missing` benign reason + `/3` validation/render in `pulse.py` |
| C3 | Antigravity single transcript, `model`, `cache_read_tokens`, `ANTIGRAVITY_CONVERSATION_ID` | C2 | `_intent/identity.py` precedence swap, `_enumerate_antigravity`, `_antigravity_usage`, `read_records`, `custom_session_routines.md` |
| C4 | Twin sync, vendor-neutral READMEs, changelog, lockfile, narrow promise & negative tests | C3 | Byte-identical `templates/` twins, docs, `cairn-lock.yml`, updated & new tests in 4 test files |

## Acceptance criteria

- **C1:** `_RATIO_INDEX`, `RATIO_VERSION`, `_ratio_index_copy` removed from `meter.py`. `_safe_config_path` refuses Windows UNC/device prefixes (`\\`, `//`, `\\?\`, `\\.\`) before filesystem calls; `validate_config_bytes` accepts optional `models_config` and rejects paths equal to or inside configured `projects[i]["path"]` or `sources[i]["root"]`. `_read_account_json` checks `_is_link` on parent directory and file, opens with `O_NOFOLLOW | O_NONBLOCK`, and verifies `S_ISREG` + `(st_dev, st_ino)` == `lstat`; bare `meter.py [--json]` validates `meter.json` without opening `models_config`. `validate_models_config_bytes` enforces closed schema `cairn-meter-models/1` (`<= 128` models, `<= 32` distinct non-overlapping prefixes per model, `<= 128` `tier_rules`, configurable `tiers` default `["high", "medium", "low"]` excluding `"unknown"`/`"unspecified"`, strict int weights `0 <= num <= MAX_COUNTER` and `1 <= den <= MAX_COUNTER`, explicit `cache_write_mode` `"ttl_split"` vs `"unbilled"`, `1 <= over_tokens <= MAX_COUNTER`, and validated `tools.antigravity`). Missing unconfigured default degrades (`models_config_missing`, `weighted=None`, `tier="unknown"`, `reference_index=None` + all-`None` `reference_tokens`); missing explicit or bad/linked config raises `Unavailable("config_invalid")`. `"unbilled"` emits `"0"` for `cache_write` only when `kinds["cache_write"] in (None, 0)` and `fresh_input`, `cache_read`, and `output` are non-`None`. `_resolve_model_tier` checks exact `models[m].tier`, unambiguous `models[*].prefixes`, then unambiguous `tier_rules` (`prefix`, then hyphen-split lowercase `segment`), failing ambiguous ties to `"unknown"`. `cairn-meter-ledger/6` (`cairn-source-readers/6`) migrates in place to `/7` preserving events/daily sums without global overwrites (`/3`–`/5` still `ledger_old_schema`). `dev/.cairn/meter-models.json` and `dev/.cairn/model-selection-mapping.yml` map `Fable`/`Astra`/`Carbon` to `frontier`.
- **C2:** `_project_export` emits `cairn-meter-project/3` with `ratio_version` (nullable when unconfigured), `"tier"` on every row (including folded `daily` rows, from `effective_model` else `selected_context` `model`), and ordered `"by_tier"` (`models_config["tiers"]` then `"unknown"`, `[]` when empty) summing counts and `Fraction` weights with existing `None`-propagation. `pulse.py` includes `models_config_missing` in `_PULSE_BENIGN_REASONS`, renders `/1` and `/2` unchanged, validates `/3` (consistent `by_tier`, `"unknown"` last if present, nullable `ratio_version` on `/3` only, any safe `tier` string in `r"[a-z][a-z0-9_-]{0,31}"`), and prints `tier=...` plus `gauge: usage by tier ...`.
- **C3:** `HARNESS_SESSION_VARS` puts `("antigravity", "ANTIGRAVITY_CONVERSATION_ID")` before `("antigravity", "ANTIGRAVITY_TRAJECTORY_ID")`. `_enumerate_antigravity` enumerates only `brain/<uuid>/.system_generated/logs/<log_filename>` (default `"transcript.jsonl"`, validated via `_windows_component` and `r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\.jsonl"`, charging 1 entry per log check against `MAX_ATTRIBUTION_RUN_ENTRIES`, skipping `transcript_full.jsonl`). `_conversation_project` honors bounded `tools.antigravity` `lead_factor` (`2..1000`), `max_bytes` (`1..128 MiB`), `max_entries` (`1..20_000`). `_antigravity_usage` and `read_records` extract optional top-level `model` (`_safe_alias`, `model_provenance="usage_record"`, `effective_model=model`) and optional configured `cache_read_field` (`cache_read_tokens`, `r"[A-Za-z_][A-Za-z0-9_]{0,63}"` excluding `input_tokens`, `output_tokens`, metadata keys) into `kinds["cache_read"]`; invalid present values flag `invalid_record`. `cache_read_tokens` joins [`dev/rules/custom_session_routines.md`](../rules/custom_session_routines.md).
- **C4:** Twin files compare identical with `cmp`. Templates pass `tests/quality_gate.py --sub neutrality` (exit 0). Lockfile advances via `upgrade --finalize` and `install/verify_integrity.py --target .` exits 0. Updated and new narrow tests in `test_meter.py`, `test_gauge.py`, `test_intents_tool.py` (clearing `ANTIGRAVITY_CONVERSATION_ID` in `_IDENTITY_VARS`), and `test_model_selection_stub.py` (validating `dev/.cairn/meter-models.json` vs `model-selection-mapping.yml`) pass; negative controls fail under scratch one-line mutations.
- **Security preflight delta & scientific check:** S1–S5 hold from the accepted proposal with two additions: configurable `tiers` accepts only lowercase safe identifiers excluding `"unknown"`/`"unspecified"`, and `tier_rules` supports exact hyphen-segment matching (`split("-")`, no regex/ReDoS) so effort suffixes (`gemini-4-neon-high`) never match tier labels. Independent scientific check: `N/A: no scientific assumption or result touched.`

## Scope delta

**Scope delta**: preserved

## Verification

Run once on macOS (`/Users/kendal30/conda_envs/lhm/bin/python3.13`) in the implementation worktree after C4 (no pre-change baseline or wide group):
- `pytest -q -p no:cacheprovider -rfsE tests/integration/test_meter.py tests/test_meter_claude_usage.py tests/test_meter_usage_free_records.py tests/integration/test_gauge.py tests/test_intents_tool.py tests/test_model_selection_stub.py`
- `python dev/tools/check_model_selection.py`
- `python tests/quality_gate.py --sub neutrality`
- `cmp dev/tools/meter.py templates/skills/_lib/meter.py && cmp dev/tools/pulse.py templates/skills/_lib/pulse.py && cmp dev/tools/_intent/identity.py templates/modules/team-gated/_intent/identity.py`
- `python install/verify_integrity.py --target .`
- `python tests/check_cairn.py dev/measurement/README.md templates/core/dev/measurement/README.md dev/rules/custom_session_routines.md CHANGELOG.md dev/plans/2026-11-22-config-driven-meter-tiers-and-antigravity.md`
- `python dev/tools/sync_doc_snippets.py --check`
- Post-merge live check: install `~/.cairn/meter-models.json`, test v6->v7 migration on a disposable copy of the backed-up ledger, move live `~/.cairn/meter/ledger.json` aside cleanly, run `meter.py --json` and `meter.py refresh --report --json`, and confirm `cairn-meter-project/3`, `frontier`/`high`/`medium`/`low` tiers, and Antigravity counts match.

## Plan review -- Gemini 4 Neon (Reviewer) -- 2026-11-22

```
Reviewed commit: fb951b19f45fdbc7065f04ac09013fee13470630
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: ~7m
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes — the 4-chunk plan delivers all accepted Decision commitments (v0.8.1, `frontier` tier for `Fable`/`Astra`/`Carbon`, `cache_read_tokens`, post-landing W1 backup), with two C1/C2 contract gaps (B1–B2) that block clean Low-tier execution -- checked `dev/proposals/archive/2026-11-22-neon-config-driven-meter-tiers-and-antigravity.md:215-231`, `dev/tools/meter.py:1948-2010, 2374-2407, 4089-4141`, `dev/tools/pulse.py:291-470`.
2. **Best alternative.** Keep the 4-chunk sequence as framed; no simpler path delivers config-driven weights, configurable tiers, v6->v7 migration, and Antigravity fixes together -- verified `dev/tools/check_model_selection.py:155-235` and `tests/test_model_selection_stub.py:154-231` already accept `tier: frontier` without checker edits.
3. **What would show it wrong.** Cross-model prefix overlaps slipping past validation, Antigravity models staying `weighted=None`, unconfigured `_add_rows` failing `ledger_invalid`, or `pulse.py` rejecting `meter.py`'s `by_tier` -- checked `dev/tools/meter.py:941, 2393-2395, 4092`, `dev/tools/pulse.py:354`.

**Does any rule weaken or disappear?** No: adding `cache_read_tokens` to `dev/rules/custom_session_routines.md:44-54` preserves its allowlist, `docs/methodology/roles.md` stays untouched, and `tests/quality_gate.py --sub neutrality` currently exits 0 (verified).

**Pareto 80/20 test check:** Pass — Verification runs only the 6 directly affected test files plus targeted checks (`check_model_selection.py`, neutrality, twin `cmp`, `verify_integrity.py`, `check_cairn.py`, `sync_doc_snippets.py --check`) with no full-suite bloat.

**Findings**

1. **B1 (Blocking — C1 validation & weight-prefix contract):** C1 enforces non-overlapping prefixes only "per model" (missing cross-model overlaps required by Proposal S2), omits prefix lookup in `_weighted_reference_tokens` (leaving Antigravity's suffixed `model` names unweighted), and omits `tiers` bounds/membership validation (allowing a `tier` outside `tiers` to drop out of `by_tier` and fail `pulse.py`).
   - *Exact closure*: In C1, replace `<= 32 distinct non-overlapping prefixes per model` with `<= 32 distinct prefixes per model with no exact or prefix overlap across all models[*].prefixes`; replace `configurable tiers default ["high", "medium", "low"] excluding "unknown"/"unspecified"` with `configurable tiers (1..32 distinct r"[a-z][a-z0-9_-]{0,31}" strings, default ["high", "medium", "low"], excluding "unknown"/"unspecified"; every models[m].tier and tier_rules[i].tier must be in tiers)`; and add before `_resolve_model_tier`: `_weighted_reference_tokens resolves exact models[m] before unambiguous models[*].prefixes (failing closed to None).`

2. **B2 (Blocking — C1/C2 `_add_rows`, `_load_ledger`, and `by_tier` parity):** `_add_rows` (`dev/tools/meter.py:2393-2395`) references removed `RATIO_VERSION`; when `models_config` is `None`, merging two differently-indexed daily rows into `reference_index=None` with non-`None` `reference_tokens` violates `_validate_aggregate_row` and fails `_atomic_replace_ledger` (`941`). `_load_ledger` also needs `(ratio_version is None) == (ratio_index is None)` and exact `(schema, reader_version)` pair checks. In C2, `by_tier` omits zero-event-tier rules and non-terminating weight rounding parity (`meter.py:4092` rounds to 28 digits, causing raw `Fraction` comparison in `pulse.py` to reject valid `[1, 3]` exports).
   - *Exact closure*: Append to C1: `_load_ledger requires (ratio_version is None) == (ratio_index is None) and exact (schema, reader_version) pairs (/6+/6 or /7+/7); _add_rows takes current ratio_version and sets reference_tokens to all-None whenever resulting reference_index is None.` In C2, change `ordered "by_tier" (models_config["tiers"] then "unknown", [] when empty)` to `ordered "by_tier" containing only tiers with events >= 1 (models_config["tiers"] then "unknown", [] when empty)` and change `consistent by_tier` to `consistent by_tier matching exact aggregate tiers (events >= 1, len <= 33, excluding "unspecified", comparing sums via _fraction_text parity)`.

3. **N1 (Non-blocking — C4 existing test updates):** In `tests/integration/test_meter.py`, 11 Antigravity tests (`L1370`, `L4867`–`L5346`) write `a.jsonl`/`x.jsonl`/`y.jsonl`/`z.jsonl` (with `L5106` asserting `2 + 3` entries from `scandir(logs)`), and `L1784`, `L2164`–`L2297`, `L4251`–`L4295` use removed `_RATIO_INDEX`/`RATIO_VERSION` or unconfigured homes; update them alongside C4 (migrating to `transcript.jsonl`, converting `y.jsonl` to a `transcript_full.jsonl` skip check, and updating `L5106` to `2 + 1`).

**Not covered**: Internal Security Review pass (separate required review), `pytest` execution, and private `~/.cairn/`/`~/.gemini/` files (ran `quality_gate.py --sub neutrality`, twin `cmp`, `verify_integrity.py`, `claim_check.py`, `check_cairn.py`, and a 28-digit `Decimal`/`Fraction` check). Exceeds the 300-word target to supply exact one-round closure text for B1–B2.
