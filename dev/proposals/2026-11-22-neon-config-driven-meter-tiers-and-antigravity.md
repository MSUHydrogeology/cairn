# Config-driven model weights, agent-tier reporting, and Antigravity reader fixes

**Author**: Gemini 4 Neon (Author; Maintainer-selected session)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — alters three shipped tools (`meter.py`, `pulse.py`, `_intent/identity.py`) and adds an external model and adapter configuration file
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-22
**Rules that apply**: dev/rules/protected-surfaces.md, dev/rules/working-agreements.md, dev/rules/conventions.md, dev/rules/custom_session_routines.md, dev/rules/development-environment.md
**In brief**: Move model pricing weights, Claude and multi-vendor tier mappings, and bounded reader settings out of Python into an account-owned JSON config, add token-category and agent-tier breakdowns to meter and pulse reports, and fix Antigravity's transcript, model, cache-read, and session-identity gaps.

Proposed paths:
- `dev/.cairn/meter-models.json`

## Decision summary

**Today's usage meter hardcodes vendor prices in Python, omits agent-tier totals (`high`, `medium`, `low`), and misses most Antigravity tokens plus its `model` and session link.** [`dev/tools/meter.py`](../tools/meter.py) embeds 15 model tables (`_RATIO_INDEX`), ignores Antigravity's `model` field and an unapproved cache-token field (`92.6%` of Antigravity volume), reads duplicate `transcript_full.jsonl` files, and misses Antigravity's live session ID in [`dev/tools/_intent/identity.py`](../tools/_intent/identity.py).

We propose moving model pricing weights, **agent-tier** rules (grouping usage by `high`/`medium`/`low` capability tier rather than raw model name), and updatable Antigravity field settings into one account-owned JSON config (`~/.cairn/meter-models.json`, with Cairn's reference file at `dev/.cairn/meter-models.json`). Meter and Pulse reports then break usage down by both token category (`fresh_input`, `cache_read`, `cache_write`, `output`, `weighted`) and agent tier (`by_tier`), composing cleanly with v0.9's [cost-per-plan](2026-11-22-claude-cost-per-plan.md). Clearing vendor examples from [`templates/core/dev/measurement/README.md`](../../templates/core/dev/measurement/README.md) also resolves 7 of 8 template neutrality-gate failures. Four Maintainer choices end the Proposal section.

## Context

- **Hardcoded built-ins and neutrality failures.** [`dev/tools/meter.py`](../tools/meter.py) (lines 68–174) hardcodes `_RATIO_INDEX` (15 models). [`templates/core/dev/measurement/README.md`](../../templates/core/dev/measurement/README.md) (lines 45–59) repeats those vendor names, causing 7 of 8 failures in `tests/quality_gate.py --sub neutrality --report`. [`dev/.cairn/model-selection-mapping.yml`](../.cairn/model-selection-mapping.yml) assigns `Opus`/`Sol`/`Argon`, `Sonnet`/`Terra`/`Neon`, and `Haiku`/`Luna`/`Hydrogen` by family, omits `Fable`, and is never read by `meter.py`.
- **Missing agent-tier reporting.** Sanitized `dev/measurement/meter.json` (`cairn-meter-project/2`) gives counts and `weighted` totals by `(week, day, artifact, tool, model)`, with no agent tier or `by_tier` summary in `meter.py` or [`dev/tools/pulse.py`](../tools/pulse.py).
- **Measured Antigravity gaps.** Count-only measurements on this Mac ([`dev/measurement/antigravity-log-fields-2026-11-22.md`](../measurement/antigravity-log-fields-2026-11-22.md)) show: (1) `46 of 46` `transcript.jsonl` / `transcript_full.jsonl` pairs have identical token records; (2) `37 of 38` records on `2026-11-22` carry top-level `model` (ignored by `meter.py`; `0 of 30` checked match `_RATIO_INDEX` keys); (3) all `6,172` records contain an unapproved cache-token integer totaling `867,668,476` tokens (`92.6%` of total tokens); and (4) `ANTIGRAVITY_CONVERSATION_ID` matches `brain/<uuid>`, whereas [`dev/tools/_intent/identity.py`](../tools/_intent/identity.py) (line 47) reads only `ANTIGRAVITY_TRAJECTORY_ID`.

## Proposal

Two outcomes in one four-chunk plan, standard-library-only, touching no scaffold installer code:

### Outcome 1 — Config-driven weights, Claude/multi-vendor tiers, and `by_tier` reports

1. **Account-owned model config (`cairn-meter-models/1`).** Remove `_RATIO_INDEX` and vendor price constants from [`dev/tools/meter.py`](../tools/meter.py) and [`templates/skills/_lib/meter.py`](../../templates/skills/_lib/meter.py). Load config from optional consent key `models_config` in `~/.cairn/meter.json`, else `~/.cairn/meter-models.json` when present (via `_fixed_user_home()`, never git repo auto-discovery). Validate as a non-link regular file `<= 256 KiB` with `_unique_object`, `_reject_constant`, and closed schema `cairn-meter-models/1`. Without a config (and no explicit `models_config`), raw counting continues with `tier="unknown"`, `weighted=None`, `ratio_version=None`, and `models_config_missing`. Any missing explicit `models_config` or linked/invalid config fails closed (`Unavailable("config_invalid")`).
2. **Weights, prefixes, Claude tiers, and `cache_write_mode`.** Each `models` entry defines rational `[num, den]` weights, optional `long_prompt`, optional `tier` (`high`/`medium`/`low`), optional `prefixes`, and explicit `cache_write_mode`: `"ttl_split"` (charges 5m/1h writes) vs `"unbilled"` (`kinds["cache_write"]` stays `None` when omitted by logs, while `reference_tokens["cache_write"]` is `"0"`, enabling `reference_tokens["total"]` unless a non-zero `cache_write` appears). A bounded `tier_rules` list (`<= 128` rules) maps prefixes (including Claude families `claude-fable-`, `claude-opus-`, `claude-sonnet-`, `claude-haiku-`) to tiers so new releases get tiered without code edits. Exact keys match before prefixes; conflicting weight or tier matches fail closed (`None` / `"unknown"`). Ship Cairn's reference table at `dev/.cairn/meter-models.json` and keep template READMEs vendor-neutral.
3. **`cairn-meter-project/3` and `pulse.py` tier breakdowns.** Resolve each aggregate row's `"tier"` at export time against the active config (covering folded `daily` rows, which already retain `model`, `model_provenance`, and `effective_model`), emit `"tier"` on each aggregate row, and add top-level `"by_tier"` (observed tiers ordered `high`, `medium`, `low`, `unknown`, summing `events`, `unknown_events`, `kinds`, and `reference_tokens` with the existing `None`-propagation rule). Update [`dev/tools/pulse.py`](../tools/pulse.py) and its twin to accept `/1`, `/2`, and `/3` (allowing `ratio_version: None`, checking `by_tier` matches grouped aggregates), printing `tier=...` and `gauge: usage by tier ...`. Rows compose cleanly with v0.9's [cost-per-plan](2026-11-22-claude-cost-per-plan.md).
4. **Ledger migration (`cairn-meter-ledger/7`).** Bump `LEDGER_SCHEMA` to `cairn-meter-ledger/7` and `READER_VERSION` to `cairn-source-readers/7`, migrating version-6 ledgers in place on load while preserving all events, cursors, reply counts, and daily sums; allow `ratio_version: None` when unconfigured.

### Outcome 2 — Antigravity reader and session identity fixes

5. **Identity order.** In [`dev/tools/_intent/identity.py`](../tools/_intent/identity.py) (line 47) and [`templates/modules/team-gated/_intent/identity.py`](../../templates/modules/team-gated/_intent/identity.py), place `("antigravity", "ANTIGRAVITY_CONVERSATION_ID")` before `("antigravity", "ANTIGRAVITY_TRAJECTORY_ID")` in `HARNESS_SESSION_VARS`.
6. **Single transcript and bounded adapter settings.** In `_enumerate_antigravity`, read only `tools.antigravity.log_filename` under `logs/` (default `"transcript.jsonl"`, single-segment `.jsonl` name), skipping `transcript_full.jsonl`. Read optional `lead_factor >= 1`, `max_bytes <= 128 MiB`, and `max_entries <= 20,000` within those hard code ceilings. Stateful tool parsers stay in Python.
7. **Antigravity `model` and cache-read extraction.** Extract top-level `model` via `_safe_alias` on Antigravity token records. Under Choice 2, run one authorized count-only fixed-candidate lookup to name the cache-token key, add it to [`dev/rules/custom_session_routines.md`](../rules/custom_session_routines.md), configure `tools.antigravity.cache_read_field`, and extract non-negative integers into `kinds["cache_read"]`.

### Choices for the Decision

1. **Release placement:** **v0.8.1** before the cut (clears template neutrality and fixes Claude/Antigravity reporting now), OR **v0.9** beside [cost-per-plan](2026-11-22-claude-cost-per-plan.md) (fixing template README prose separately before v0.8.1).
2. **Antigravity cache-read key:** Authorize one count-only lookup to name the cache-token key (`92.6%` of tokens), add it to [`dev/rules/custom_session_routines.md`](../rules/custom_session_routines.md), and extract `cache_read` (**Recommended**), OR leave `cache_read=unknown`.
3. **Claude `Fable` tier:** Assign `Fable -> high` in [`dev/.cairn/model-selection-mapping.yml`](../.cairn/model-selection-mapping.yml) and `dev/.cairn/meter-models.json` (**Recommended**), OR keep `unknown`.
4. **Tier:** Heavy, as proposed.

## Rationale

Moving volatile pricing, tier rules, and field names into an account-owned JSON config eliminates vendor-specific built-ins from shipped Python without violating the standard-library-only rule or reading unconsented repository trees. Skipping `transcript_full.jsonl` halves Antigravity log I/O with proven token parity.

## Alternatives considered

- **Keep `_RATIO_INDEX` in `meter.py`:** Rejected; forces code edits and neutrality-gate failures per model release.
- **Parse `dev/.cairn/model-selection-mapping.yml` directly:** Rejected; needs PyYAML (optional) or fragile bespoke YAML parsing, and mixes project prose config into private account accounting.
- **Keep reading `transcript_full.jsonl`:** Rejected; duplicates all 46 paired logs and risks >8 MiB line drops.

## Documentation / doctrine surface

- **Governing layer:** None (`AGENTS.md`, `docs/methodology/` untouched).
- **Deliberation layer:** [`dev/rules/custom_session_routines.md`](../rules/custom_session_routines.md) (only if Choice 2 adds one key name), `dev/.cairn/meter-models.json` (new), [`dev/.cairn/model-selection-mapping.yml`](../.cairn/model-selection-mapping.yml) (if Choice 3 adds `Fable`), [`dev/PLANNING.md`](../PLANNING.md).
- **Descriptive layer:** [`dev/measurement/README.md`](../measurement/README.md), [`templates/core/dev/measurement/README.md`](../../templates/core/dev/measurement/README.md), [`CHANGELOG.md`](../../CHANGELOG.md).

## Evidence / verification plan

**Falsification:** Live Mac refresh shows Claude `opus` (`high`) and `sonnet` (`medium`) matching `by_tier`, Antigravity `2026-11-22` records reporting `model`, `tier`, `cache_read` (under Choice 2), and `weighted` totals matching an independent count, and `tests/quality_gate.py --sub neutrality` dropping the 7 [`templates/core/dev/measurement/README.md`](../../templates/core/dev/measurement/README.md) failures to 0.

### Tests required

Narrow tests in [`tests/integration/test_meter.py`](../../tests/integration/test_meter.py), [`tests/integration/test_gauge.py`](../../tests/integration/test_gauge.py), [`tests/test_intents_tool.py`](../../tests/test_intents_tool.py), and [`tests/test_model_selection_stub.py`](../../tests/test_model_selection_stub.py):
1. Config validation & weights: absent default (`models_config_missing`), fail-closed explicit missing/linked/oversized/malformed/conflicting-prefix configs, `"unbilled"` vs `"ttl_split"` cache-write mode with negative controls.
2. Tier resolution, `cairn-meter-project/3` `by_tier` with `None`-propagation, `pulse.py` `/1`/`/2`/`/3` acceptance and tampered-`by_tier` rejection.
3. Version-6 ledger migration preserving reply counts and daily totals.
4. Antigravity `ANTIGRAVITY_CONVERSATION_ID` precedence, single `transcript.jsonl` read, `model` and `cache_read` extraction, and `log_filename` traversal refusal.
5. Cairn self-check ensuring `dev/.cairn/meter-models.json` validates and matches tier assignments in [`dev/.cairn/model-selection-mapping.yml`](../.cairn/model-selection-mapping.yml).

### Examples / smoke checks

`python tests/check_cairn.py`, `python tests/quality_gate.py --sub neutrality`, `cmp` across twin files (`meter.py`, `pulse.py`, `_intent/identity.py`), and `python install/verify_integrity.py` after lock update.

#### Security preflight — five questions, answered in writing

- **S1 — Who supplied it?** Pricing tables, tiers, and bounded adapter settings arrive only from `~/.cairn/meter-models.json` (via `_fixed_user_home()`) or explicit consent `models_config`, never git repos or logs. Token counts and model strings arrive from consented logs; session IDs come from process env and are hashed before hitting `dev/intents.jsonl`.
- **S2 — Can it fail?** Yes: negative controls supply linked/oversized/malformed/conflicting-prefix configs, missing explicit `models_config`, traversal `log_filename`, non-zero `cache_write` on `"unbilled"`, and tampered `by_tier` in `pulse.py`, each verified failing under a one-line mutation.
- **S3 — What fires it, over what?** `meter.py refresh` / `refresh --report` / `rebuild` and `pulse.py` / `tests/gauge.py --pulse` validate all consented roots, `models_config`, and exported JSON. Both READMEs will state: *"Pricing weights, tier rules, and adapter field settings load only from `~/.cairn/meter-models.json` or an explicit `models_config`; without one, raw token counts stay intact while `tier` and `weighted` stay unknown."*
- **S4 — Which way does it break?** Missing unconfigured default degrades precision (`models_config_missing`, `tier="unknown"`, `weighted=None`); explicit missing or invalid/linked config fails closed (`Unavailable("config_invalid")`); ambiguous prefixes yield `None`/`"unknown"`; invalid log `model` or `cache_read` flags `invalid_record`; missing `ANTIGRAVITY_CONVERSATION_ID` falls back to `ANTIGRAVITY_TRAJECTORY_ID`.
- **S5 — Who still wins?** A writer who can alter local logs can spoof counts/model IDs in reports, and a writer who can edit `~/.cairn/` already controls consent. Repo config injection, `log_filename`/`models_config` path traversal, and silent cross-vendor misweighting are closed by construction.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Real Claude or Antigravity replies land in `tier=unknown` despite populated config; weighted totals disagree with independent sums; a migrated version-6 ledger alters prior daily totals; or editing `~/.cairn/meter-models.json` frequently triggers `config_invalid`.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance
