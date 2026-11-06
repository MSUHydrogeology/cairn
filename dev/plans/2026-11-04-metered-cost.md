# Plan: Meter real cost without collecting conversations

**Source proposal**: dev/proposals/archive/2026-10-30-claude-metered-cost.md
**Author**: Sol (security/design plan author; high)
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Measure opted-in agent usage and report team and test cost for v0.7; budget enforcement follows in v0.8.
**Elapsed**: 5m21s (17:26:08-17:31:29 UTC; finalization excluded)
**Tokens**: unknown

## Source proposal

The heavy Decision accepts the revised meter, weekly pulse, cooperative
unattended stop and conditional Tokens retirement; Elapsed stays until
equivalence. Operative text, MC1-MC3/MS1-MS2 response and Decision are preserved;
opening archives the source unchanged.

The November 5 Maintainer disposition below moves only the spending guard and
unattended launcher to v0.8. The current v0.7 contract is measurement, reporting,
handoff refresh and the existing comparison/conditional-retirement checks.
The [joint v0.8 proposal](../proposals/2026-11-05-codex-budgeted-unattended-work.md)
must be current and linked at closeout; its later review, Decision and
implementation do not keep this plan open. Archived source records stay intact.

## Scope

- `bootstrap/tests/integration/test_meter.py`

Untracked paths:
- `dev/measurement/meter.json`

One standard-library collector, `tools/meter.py`, with small tool readers
(tool-specific `vendor-ok` annotations),
private per-user configuration/ledger outside repositories and project-only
gitignored aggregates.
No proxy, daemon, dependency adoption, per-artifact agent targets or scores.
No host configuration, private-log access, signing or baseline change now.

Tool coverage includes Claude, Codex and Antigravity. Report each tool's
available measurements and unknown fields separately; unsupported Antigravity
usage is not zero and cannot disappear from a purported complete team total.
The November 5 permission covers only the recorded source investigation below,
not ongoing collection or the later private trial.

**Reuse.** Searches found `tools/gauge.py`, `tools/audit_report.py` and
`scripts/token_budget.py`, not a usage collector. Reuse session display/file
safety, replacing whole-file reads with capped streaming. Read
`tools/_intent/identity.py` digests and `tools/_intent/record_io.py`
claim/release intervals; intent producers/pruning and shipped twins stay unchanged.

The [measurement strategy](../strategy/2026-10-27-antigravity-lightweight-team-measurement.md)
feeds pulse size/side-file attribution and always-loaded estimates. Broader
audit-reporter changes, product-classifier correction and measurement-archive
installation are not authorized by the meter Decision: return those uncovered
items to parent-owned board reconciliation for proposal, not silent completion.
These uncovered outcomes remain in the existing grouped `dev/PLANNING.md`
row **2b**, with retirement coordination in row **12**; the parent must retain
that full v0.7 row until disposition. This plan does not claim their delivery.
Suite reporting is produced by 2b from existing JUnit XML and the tier map,
independently of 2a; 2a can consume that pulse without an interface prerequisite.

**Delivery (ordinary 2; MSP3).** Add only the self-contained, byte-identical
`templates/skills/_lib/meter.py` -> `tools/meter.py` pair to
`bootstrap/_scaffold/config.py`'s existing `_SKILLS_MAPPINGS`; its existing
`bootstrap/_scaffold/install.py` install/upgrade consumers deliver it like
session/board, with no new module or installer framework. The collector uses
stdlib file/display patterns locally, not imports from an uninstalled helper.
Add only `dev/measurement/meter.json` to `_SKILLS_GITIGNORE`; no installer
creates local consent, policy or a private ledger. Gauge remains the existing
self-hosted reporting command; project aggregates are also readable as meter JSON.

### Documentation / doctrine surface

Describe usage/privacy in `dev/measurement/README.md` and correct the outdated
measurement description in `docs/methodology/rationale.md`.
No v0.7 admission rule or session-start spending check is added. Handoff touches
`.agents/skills/session-end/SKILL.md`, `templates/skills/session-end/SKILL.md`
and byte-identical `tools/session.py`/`templates/skills/_lib/session.py`.
Conditional Tokens edits cover `dev/proposals/_template.md`,
`dev/plans/_template.md`, `templates/core/dev/proposals/_template.md` and
`templates/core/dev/plans/_template.md`, plus `AGENTS.md` and
`templates/core/AGENTS.md`. The live-prescription search also read
`dev/agent_collaboration.md`, `templates/core/dev/agent_collaboration.md` and
`docs/methodology/dual-review.md`: these currently contain no token-use reporting
requirement. Recheck them at retirement, not by assumption. The remaining live
manual token request is `bootstrap/REANCHOR_RUNBOOK.md`'s forward-review commands:
remove that request and make `scripts/repin.py`'s `--tokens` optional with
`unknown` compatibility metadata, preserving existing record/signature schemas
and all approval checks. No ceremony, pin or signing operation is part of this
plan. Historical records and Elapsed remain intact.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C3 first | Public pulse and test-cost reporting | Author fold; independent of private collection and 2a completion | Gauge/JUnit adapter with explicit unknown usage and comparison labels |
| C1 | Constrained collector and local configuration contract | Folded reader/privacy contracts; synthetic fixtures only until opt-in | Disabled-by-default collector and delivered twin |
| C2 | Accounting, attribution and refresh | C1 | Incremental ledger, claim retention, handoff integration |
| C3 join | Join measured usage to the public pulse | C2 | Weekly/project/item/model reporting and honest coverage |
| C4 | Executable comparisons, conditional retirement and closeout | C1-C3; MAINTAINER-GATED actual private trial only | Required comparisons, earned Tokens retirement and current v0.8 proposal handoff |

Low-tier agents execute reviewed contracts on synthetic data; new
privacy judgment returns to high. Private-data work never downshifts
across its governance boundary. Configuration/policy remain the Maintainer's
choice. On reaching missing opt-in, record the normal Waiting line, continue
independent preparation, then wait; neither
acceptance nor this opening chat supplies consent.

## Acceptance criteria

**C1. Privacy/policy (ordinary 1; MSP1-MSP2).** Only a private per-user
configuration at `~/.cairn/meter.json`, outside repositories, can enable collection, allowlist source
roots and projects, with account filters where requested. Spending-policy
fields and admission decisions belong to the v0.8 proposal, not this collector.
The sole ledger is `~/.cairn/meter/ledger.json`, also outside repositories;
refuse linked/unverifiably private config or destinations, never relocate into a checkout.
No repository config, log field, remote, command argument or supplied aggregate
grants consent or changes that policy. Absence/disabled means no private reads.
Explicit local configuration allowlists source roots and projects, identifying
projects by credential-stripped remote. A requested account filter must match
source evidence; unavailable identity cannot be filled from the configured label.
Unfiltered approved project usage can retain account identity as unknown, never
as a verified spending account. No auto-discovery
of unlisted projects. Reject links in ancestors/leaves, non-regular inputs,
oversized lines and non-finite/negative usage. Revalidate opened identity and
bounded reads; retain no prompt, response or command text. Retention is the
closed bookkeeping set below, not arbitrary parsed fields. Strip remote
userinfo, credential query/fragment and
SCP credentials before storage; ambiguous identity
is unknown. Private directories/files use restrictive permissions; atomic writes
refuse redirected destinations and preserve old bytes on failure. Project output
contains only its own aggregates. Secret/control-byte fixtures cover bodies,
remotes, filenames, stdout/stderr and failed writes: errors identify sanitized
file aliases/line numbers, never input or exception text; names use `encode_display`.

Counters require exact JSON integers, not booleans, strings or fractional values,
in `0..2**63-1`. Reported percentages require actual finite JSON numbers,
excluding booleans/strings, in `0..100`; they are not admission authority.
Reject duplicate JSON keys and nonstandard NaN/infinity constants. Parse source
ISO timestamps explicitly; never coerce numeric strings, use file mtime or
replace observation time with collection time. Malformed/unsupported records
that carry usage mark affected coverage unknown, not
silently skip to zero. Known non-usage content records are discarded.
Map source project identity only to an allowlisted local project, then compare
its stripped Git remote; never execute Git in an arbitrary source-supplied cwd.

### Reader contracts (ordinary 1; MSP1)

Non-private evidence read 2026-11-04: [Claude reader and fixtures](https://raw.githubusercontent.com/ccusage/ccusage/main/rust/adapters/claude/src/lib.rs),
[Claude cache semantics](https://platform.claude.com/docs/en/build-with-claude/prompt-caching),
[Codex rollout reader notes](https://raw.githubusercontent.com/ccusage/ccusage/main/rust/adapters/codex/src/README.md)
and [Codex protocol](https://raw.githubusercontent.com/openai/codex/main/codex-rs/protocol/src/protocol.rs).
These establish shapes, not this host's versions. Implement only proven shapes;
unsupported extensions/compression or missing required fields produce unknown.

| Source shape | Extraction and synthetic expected result |
|---|---|
| Claude JSONL `type=assistant`, `timestamp`, `sessionId`, optional `requestId`, `message.{id,model,usage}` | `usage` has `input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens`. `(10,4,2,8)` stays four disjoint kinds; physical input is 20, not 10. TTL subdivisions, when present, must sum to cache creation; do not add them again. |
| Codex JSONL `type=event_msg`, `payload.type=token_count`, `payload.info.{total_token_usage,last_token_usage}`; model from `turn_context` | Input includes cached reads; `(input=20,cached=8,output=4)` gives fresh input 12, cache-read 8, output 4; reasoning is an output subset. Missing cache-write semantics stays unknown, not zero; do not invent a weighted total for it. A cumulative sequence 20,20,35 contributes 35, not 75. |
| Observed Codex JSONL `type=event_msg`, `payload.type=item_completed`, `payload.{started_at_ms,completed_at_ms}`, `payload.item.{type,id,command,cwd,exit_code}` with item type `CommandExecution` | This timing shape is persisted locally, not merely a protocol event. Classify only direct `pytest` or `python[3[.minor]] -m pytest` command arrays; synthetic endpoints 1000/3500 yield 2.5 seconds. Distinct repeats count; overlapping intervals union for wall wait. The sampled commands were shell-wrapped, so their pytest classification remains unknown. Absent endpoints, negative intervals and unsupported shapes are unknown. Inspect only command classification transiently; retain class/id/times, never argv/output. `task_complete.duration_ms` is turn duration, not test execution time. |
| Observed Cairn-indexed Antigravity transcript JSONL `step_index, source, type, status, created_at`, with optional content/tool-call fields | The metadata-only sample established a step timeline, not token/cache counters or command execution duration. Do not inspect content or treat absent usage as zero. The [documented CLI status-line payload](https://antigravity.google/docs/cli/statusline) describes context-window counters, quota and estimated cost, but does not prove their persistence in these logs. No status-line capture, configuration change or live quota request is authorized by the inspection. Keep usage/cache semantics and any missing timing unknown until a supported source is established. |

Claude repeated message/request ids count once across copied files; requestless
provider message ids require session/lineage proof, not a filename guess.
Conflicting usage revisions are unknown, not summed or maximized. Codex uses
cumulative differences once, with `last` only as reconciliation, never as an
additional charge. Replay prefixes end at proven task/trigger markers; unknown
fork baselines refuse rollup. Separate compaction usage is counted only once
against its response/compaction id, or coverage is unknown. Child contributions
roll into parents once; unsupported lineage remains explicitly unattributed.
Tests include parent 100, child inherited 100 then 130: contribution 30, not 130.

**Deferred source blocker -- ordinary 1/MSP1, spending admission.** No supported local input yet proves
the spending account *at observation time* and that reading's source observation
time. Codex `creator_account_id` is creation-only and never updated on resume;
`rate_limits` has bucket/window/reset/percentage but no account or observation
time. Claude's [status-line data](https://code.claude.com/docs/en/statusline)
exposes percentages/reset times, not that binding either. Do not substitute
policy's account label or the enclosing event timestamp as proof. Public
[account/rate-limit RPC documentation](https://developers.openai.com/codex/app-server)
describes another, live transport, not a persisted-log contract; adding its
authenticated calls/capture is not silently authorized here. The v0.8 proposal
retains the need for evidence carrying both bindings before unattended
admission. The approved November 5 metadata sample
establishes the persisted command timing shape above. It does not establish
pytest attribution for shell wrappers; keep that coverage unknown and use the
existing JUnit adapter for independently recorded test durations. Usage counts,
command elapsed time, test duration and account-bound spending admission are
different quantities. The account/time binding blocks the deferred guard, not
v0.7 raw counting or public reporting. No private trial or automatic admission
is authorized; no configuration label becomes a provider observation.

The v0.8 proposal carries this normalized admission fixture, not a claimed vendor record:
`{source:s, account:a, unit:plan-percent, window:[start,reset], value:24.5,
observed_at:t, coverage:complete}`. Policy separately selects the same source,
account, unit/window, limit 80 and age 60 seconds. At `now=t+30` it admits;
`true`, `"24.5"`, absent account/time, wrong window or `now=t+61` refuses.

**C2. Accounting/retention (ordinary 1-2; MSP2-MSP3).** Namespace/deduplicate message ids across repeated/rotated files; retain
input, output, cache-write and cache-read separately with tested input/cache
inclusion semantics. Reconcile per-turn and final running totals, never sum
snapshots; subtract inherited baselines and roll child usage into parents once.
Persist claim mappings on first observation, before pruning; digest collisions,
overlapping claims or missing intervals forbid guessed item attribution. Reliable
items get artifact totals, otherwise daily totals with explicit ambiguous/unknown
coverage, never invented zero. Timestamp-only test start/end/repeat intervals
produce test-wait time without retaining commands. Append, partial-line,
truncation, rotation and inherited-session fixtures make incremental results
equal rebuild using retained normalized history/mappings; unavailable history is
unknown. Handoff refresh precedes intent pruning; refresh failure preserves claims.
Raw kinds, a collector-local dated unit-price-ratio table (provenance and
reference token kind), and reported plan percentages remain distinct;
unknown prices/models are not silently treated as free.

The private ledger retains only: schema/reader/ratio versions; source/project
aliases and sanitized remote; hashed message/request/session/parent/call/claim
keys, separately labeled creation/observed account keys when available,
model/service-tier/cache-TTL ids, source ordinals and timestamps; four numeric
kinds with known/unknown flags, normalized cumulative checkpoints and inherited baselines; classified
test intervals; claim/release times, artifact-relative targets and mapping
confidence; cursor file identity/generation, byte offset and line number; and
one normalized history entry per logical usage event/revision needed to rebuild.
Keep the existing short session digest only for claim matching; collisions mean
ambiguous. No raw log/cwd paths, credential paths, body hashes or command strings
enter the ledger. Config maps approved root aliases; cursor names use hashed
root-relative identifiers. Project `dev/measurement/meter.json` exports only its
week/day/artifact/model aggregates, wait totals and coverage, never cross-project
ids, cursor/history or other projects' existence.

Rebuild replays retained normalized history/mappings plus approved surviving
records; a fresh empty ledger with lost logs reports unknown rather than claims
full historical recovery. On changed file identity, truncation or detected rewrite,
rescan that generation and deduplicate; never advance past a partial last line.
Append, rotation, parent pruning and replay fixtures must match full replay of
the same retained evidence. Failed durable writes leave prior ledger/cursors
unchanged. Do not prune normalized evidence while a promised rebuild needs it.

**Shipped refresh order.** Under the existing handoff owner/lock guards, surface
intents, invoke the sibling meter with the resolved interpreter, atomically
persist usage and claim mappings, then permit reflection/intent pruning. The
existing reflection-only scaffold is unchanged. A successful refresh returns
`ok`; explicitly disabled returns `disabled` without source/ledger I/O and
permits existing prune behavior. Absent collector, invalid config, failed read,
mapping coverage gap or failed atomic write returns unavailable/nonzero and
skips pruning, preserving claims; attended work and reflection remain available.
Here a mapping gap means the claim snapshot was not durably retained, not merely
uncertain item attribution: retained ambiguous mappings can still support daily
reporting. This v0.7 collector exposes no `admit` result or launcher.
`--prepare-handoff`/`--dry-run` only preview, with no private reads/writes.
Never fall back to a collector in another checkout. Enabled collection refreshes
at full handoff without needing a spending policy. Enabling never follows from
installation, this scheduling Decision or a log record.

**C3. Pulse (ordinary 3).** `tools/gauge.py --pulse` reports week/project/artifact usage and time,
test waits, review passes, model-tier mix, always-loaded cost and shared 2a suite
growth/runtime, with source/window/coverage. Count standalone review side-files
with parents; expose orphans/unspecified models. Distinguish metered tokens from
word/byte-derived estimates. Missing 2a evidence is unknown, not completed reporting.
The public-reporting slice runs before private collection: absent usage remains
unknown for each of Claude, Codex and Antigravity, not an all-zero team total.
It consumes only explicitly supplied public JUnit inputs and project aggregates,
never private usage logs or account settings. It must not invoke Git or import
code from a supplied target root. Preserve existing non-pulse gauge behavior.

2b owns the gauge adapter for existing pytest `--junitxml` reports, already used
in 2a's implementation record: `testsuite`/`testcase` attributes `classname`,
`name`, `time`, plus failure/error/skipped children. Read bounded regular XML,
reject DTD/entities, and label its testcase times as pytest total-phase seconds,
not isolated call/setup measurements. Existing `tools/test_tiers.py` inventory
supplies files/lines by tier without importing/collecting tests. Commit, Python,
selection and seed labels come from the existing verification record or explicit
report arguments; missing labels/report means unknown comparability. Gauge reads
these independently supplied inputs and prints growth/runtime alongside pulse;
no new telemetry store. Synthetic before/after XML tests can complete this
adapter before 2a finishes; 2a later supplies its actual scoped reports. Counts
of source files are never relabeled collected nodes. Neither plan is complete
without its accepted actual evidence.

Spending admission, `meter admit`, session-start spending hooks and the
unattended loop are v0.8-only work. No current output authorizes an automatic
next item. The future proposal retains fail-closed admission, private policy,
source/account/window/freshness checks and the declared overshoot/forgery limits.

**C4. Comparisons/retirement (ordinary 4).** Use normal meter `refresh --json`
and `rebuild --json` output and the existing verification record, not permanent
trial commands, a new harness or a second ledger. Test synthetically, then run
agent-owned after explicit local root/project opt-in and supported-reader checks.
The one-time inspection permission is not that opt-in. A requested account
filter remains required; absent account evidence cannot satisfy it.
Over seven days, record weighted deltas and source plan-percent readings within matched reset
windows; increases must move together beyond source rounding resolution, with
resets/missing observations visible. Record ratios, resolution and counterexamples,
not a fabricated percent conversion. Run an independently installed `ccusage`
count smoke on the same approved logs/time range and reconcile each token kind
exactly; never install/adopt it as a Cairn dependency or silently fetch it.
Missing executable/percentage/access leaves this accepted check open. The agent
compares the JSON numerically with stdlib and records exact commands, versions,
same-log coverage, dates/reset boundaries, per-kind equality and non-passes;
the comparison fails for disagreement/incomplete evidence. Retain only
sanitized aggregates. Retire Tokens only after ALL meter checks, including both
real comparisons, pass. Keep Elapsed unless timestamp evidence demonstrates the
same elapsed quantity within source resolution; unknown equivalence means retain.
At Tokens retirement repeat the live-prescription search (including collaboration
and dual-review texts), remove every still-operative self-report requirement in
the named homes, and test the real forward-review CLI without `--tokens` as well
as its legacy argument. No conflicting manual requirement may remain in force;
historical fields/schema compatibility do not require agents to fill them.

Before archive, ensure the joint v0.8 proposal exists, carries all deferred
guard/loop outcomes, source gaps and safeguards, and is linked from this plan,
the continuation plan and the board. Update it with relevant v0.7 findings.
Archive this plan and retain its already-archived source as history once the
remaining v0.7 checks pass; do not leave either old workflow live waiting for
v0.8 review, a keep-D Decision or implementation. The continuation plan can
close independently after its own A-C evidence and the same handoff requirement.

## Scope delta

**Scope delta**: Maintainer-authorized deferral of budget admission and the
unattended loop to the joint v0.8 proposal; the November 5 quote below is the
authority. No measurement privacy, accuracy, required comparison or conditional
retirement check is waived. Missing evidence for those still keeps v0.7 work open.

## Verification

Boundary A selects `python tools/test_tiers.py for <paths>` per chunk.
`bootstrap/tests/integration/test_meter.py` owns synthetic source readers,
privacy, safe reads, arithmetic, timing and disabled/unavailable CLI behavior;
falsifiers; `bootstrap/tests/integration/test_gauge.py` owns pulse grouping
and 2a evidence.
Existing canonical homes:
`bootstrap/tests/test_session_start_drain_rules.py` (no v0.7 spending/launcher activation),
`bootstrap/tests/test_session_routines.py` and `bootstrap/tests/test_session_failsafe.py`
(handoff ordering/failure), `bootstrap/tests/test_session_writes_contained.py`
(file/display safety), `bootstrap/tests/test_intents_tool.py` (digest/prune
compatibility), `bootstrap/tests/test_skills_install.py` and
`bootstrap/tests/test_skills_upgrade.py` (real delivered CLI/twin, lockfile hash
and upgrade coverage), `bootstrap/tests/test_repin.py` (conditional Tokens
compatibility). Re-resolve homes after 2a moves; preserve node identity.
Exercise actual meter, pulse and handoff CLIs on synthetic roots. No v0.7
command may launch unattended work or turn reporting into admission authority.
S2 mutations belong to C1-C3 tests; S3 is their selected pytest invocation plus
the C4 JSON comparison commands. Removing a secret filter, coverage/unit check or dedup
must fail its owning test. Other S1/S4/S5 answers remain the accepted preflight.
Target the tiny meter module below one second; record runtime misses.
The install/handoff tests exercise actual shipped success/disabled/absent/failure
branches, asserting prune invocation and durable mappings, not mocked helper
success alone. Meter tests cover bool/string rejection, no policy-from-log,
minimal retention after rotation/prune and cross-project output isolation. Gauge
tests accept existing JUnit inputs without 2a completion and fail false comparison
claims. These checks are future implementation obligations, not results here.

Ordinary and separate Security code reviews falsify committed work before
wide Boundary B: clean final commit, canonical Python 3.13.x, reviewed-range
selection plus mapped integration/workflow consumers and standing prose gates.
Record SHA/range, interpreter, clean pre/post state, commands/counts, elapsed,
tokens or unknown, non-passes, mutations and omissions. Over-10-second test
files return to 2a's slow list. Run claim, link, snippet and applicable neutrality
checks on changed prose; preserve session-copy fidelity. No full suite is
authorized here; scientific check is N/A, but both empirical C4 checks remain
required. Baseline/signing/host-policy operations are not plan-completion ceremonies.

## Plan review -- Codex Terra -- 2026-11-04

**Model**: Terra (medium)

Reviewed commit: 16191ca1c89690b6bd1dd67af1381f8f916486a5

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** Not yet: the accepted collection and stop need executable source and integration contracts before low-tier implementation -- source Proposal 1-3; plan C1-C3; findings 1-3.
2. **Best alternative.** Reuse the existing gauge and concise verification record for comparisons; dedicated trial commands need justification, not automatic rejection -- `tools/gauge.py`; plan C4.
3. **What would show it wrong?** Synthetic source records that double-count a child or admit a stale reading, or a handoff that prunes after failed refresh, would falsify the result -- source Tests required; plan C2-C3.

**Verdict**: REVISE.

1. **Blocking -- reader and observation contracts are missing.** C1-C4 name no actual tool record shapes, per-tool cache inclusion, test-command classification, or source of account-bound plan percentage and its observation time. The source requires real tool accounting and a fresh stop; low-tier execution would have to invent those decisions. Specify supported inputs, extraction and unknown/failure behavior from non-private evidence, with synthetic examples; unresolved source access stays open, not guessed.

2. **Blocking -- shipped handoff has no collector delivery contract.** C2 requires refresh before pruning, but scope changes the shipped session kernel without saying how its meter is installed or what happens when absent or disabled. The existing `tools/session.py` invokes optional `intent.py` at handoff; its shipped twin may run without a meter. Specify delivery and absent/disabled/failure behavior that preserves claims without silently losing the accepted refresh.

3. **Blocking -- shared reporting dependency is undefined.** C3 waits on a 2a reporting interface, while 2a C4 waits on 2b's shared pulse; neither names an existing interface or producer. Define an independently deliverable source, shape and ownership from existing records, plus unknown behavior, so both accepted outcomes can complete without circular waiting.

4. **Advice -- minimize trial machinery.** C4 mandates two new commands although the source requires comparisons, not a permanent trial interface. Consider existing meter output and a concise verification record if they reproduce both checks and non-passes; neither consent nor the seven-day and independent `ccusage` checks is optional.

**Elapsed**: unknown. **Tokens**: unknown.
**Covered**: accepted proposal and reviews, plan/template, strategy, gauge, session/drain and intent interfaces, 2a dependency, privacy, attribution, rotation and retirement criteria. **Not covered**: private logs, implementation, empirical comparisons, tests or the separate Security Review. The grouped product/audit/archive work remains parent-owned; this pass does not authorize it. Extra words identify three independent implementation blockers.

## Plan review -- Codex Sol (Security Review) -- 2026-11-04

**Model**: Sol (high).
Reviewed commit: 16191ca1c89690b6bd1dd67af1381f8f916486a5
Ordinary review read: e09a37a2; operative text reviewed independently.

**Tier**: Internal Security Review
**Obligation**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** Private observation and cooperative stopping deliver the Decision, but three contracts need revision before low-tier execution -- source Proposal 1/3, Response/Decision; C1-C3; MSP1-MSP3.
2. **Best alternative.** Adapt existing file/display primitives and handoff ordering, without another service or stronger quota claim -- `tools/session.py:618-677`, `_do_full_handoff`; C3 residuals.
3. **What would show it wrong?** A boolean reading admitting work, retained credentials, or pruning without durable mappings would falsify the contract -- C1-C3; numeric primitive below.

**Verdict**: REVISE.

1. **MSP1 -- Blocking: define observation versus policy.** C3/S1 require a Maintainer-controlled limit and source/account/window/observation-time match, but supported record shapes and extraction remain unspecified (ordinary finding 1). Close with non-private source contracts and synthetic examples; logs must never supply policy or opt-in. Specify numeric types, excluding booleans/strings. Python 3.12.9 primitive: JSON `true` and `false` both pass `isfinite(v) and 0 <= v < 100`; NaN/infinities fail. This is not a meter exploit.

2. **MSP2 -- Blocking: reconcile retention.** C1's retained-fields-only list excludes message/session keys, claim mappings and incremental state required by C2. The accepted source expressly permits ids. Close by naming minimal normalized bookkeeping and its private/project-output split, sufficient for deduplication, lineage and rebuild after rotation/pruning; retain no bodies, commands or credential-bearing paths. Otherwise execution must violate either privacy or accounting criteria.

3. **MSP3 -- Blocking: close shipped failure behavior.** C2 requires refresh before pruning, but `bootstrap/_scaffold/config.py:913-919` delivers session, not meter; `_prune_intents` skips absent tools. Close ordinary finding 2 with collector delivery and explicit absent/disabled/failure outcomes: opted-in refresh must durably preserve mappings before pruning, failed refresh preserves claims, unattended admission stops, attended work remains available. Exercise the real shipped consumer, not only meter helpers.

C1 already requires capped streaming rather than the helper's whole-file read, restrictive writes and sanitized diagnostics. C4 correctly preserves explicit private opt-in, seven-day/source and independent `ccusage` comparisons, and conditional retirement; no waiver is inferred.

**Elapsed**: unknown. **Tokens**: unknown.

**Covered**: committed source/reviews/Decision, template, gauge, session/drain, intent identity/pruning, installer and strategy links; only the numeric primitive ran in a separate committed copy. **Not covered**: private logs, host configuration/network, implementation checks, actual trial, platform races or suites. Mutable-log forgery/concurrent overshoot remain declared residuals. Over target to distinguish three closure conditions; parent owns other archive links.

## Response -- Sol -- 2026-11-04

**Model**: Sol (high; original security/design author).
Responds to ordinary `e09a37a2` and Security `700a1ed4`; reviews unchanged.
Operative additions answer only their findings.

- **Ordinary 1 -- partial; blocking remainder named.** Reader contracts give
  public shapes, cache inclusion, cumulative/replay rules, synthetic results
  and test-command classification. Unknown kinds/formats stay unknown. Closure
  still needs account-at-observation/time evidence and persisted test timing;
  creation metadata/protocol types cannot substitute.
- **Ordinary 2 -- settled in contract.** Existing skills mappings deliver one
  self-contained verbatim meter twin. C2 specifies success/disabled/absent/failure
  ordering; real install/handoff tests must prove durable mappings before pruning.
- **Ordinary 3 -- settled in contract.** C3 assigns the existing-JUnit/tier
  adapter to 2b. Synthetic adapter checks need no 2a output; missing actual
  evidence stays unknown and cannot complete either plan. Started 2a is untouched.
- **Ordinary 4 -- accepted.** Removed permanent trial commands. Normal JSON,
  executable numeric comparisons and concise verification records still owe
  seven-day and independent-count checks after explicit opt-in.
- **MSP1 -- partial.** C1 rejects bool/string numbers and separates source
  observations from policy. C3 tests that log fields cannot change policy or
  start another item. The shared source-binding blocker remains open.
- **MSP2 -- settled in contract.** C2's closed retention set includes hashed
  identities, lineage, claims, cursors and normalized history, with project-only
  aggregates. Rotation/prune/rebuild and secret-isolation checks falsify it.
- **MSP3 -- settled in contract.** Installation grants no consent. Failed/absent
  refresh preserves claims and forbids unattended admission; attended work
  remains available. Real shipped-consumer tests cover every branch.

Conditional Tokens retirement also covers governing text and the forward-review
CLI/runbook; historical schemas and Elapsed remain. Uncovered strategy outcomes
stay in grouped board row 2b. Status is `revising-plan`; no clearing review is
requested. No private source was read, trial run or consent/check waived.

Author checks: canonical Python 3.13.13; claim, prose-integrity, link, snippet
and neutrality gates pass; advisory rate-limit findings: none. The selector
names zero tests for this plan; no pytest/suite ran. The six external links
were read for evidence, not probed by the link gate. Review text matches
`700a1ed4` byte-for-byte, excluding the new response separator.

**Elapsed**: 11m22s (17:44:43-17:56:05 UTC; finalization excluded).
**Tokens**: unknown.

## Source investigation -- Codex Sol (HIGH) -- 2026-11-05

**Permission.** The Maintainer answered the limited, one-time, read-only
Cairn-associated metadata request in chat:

> Allow the Cairn-only metadata inspection (Recommended)

This permits only usage counters, timestamps, project/account identifiers and
test-command timing metadata, with sanitized shapes/findings retained. It does
not permit inspecting conversation text, command output, credentials or other
projects, enabling ongoing collection, or running the later private trial.

The initial inspection used read-only SQLite queries restricted to the exact
Cairn working directory, three associated Codex logs and one Cairn Claude log.
Each initial log sample was bounded to its last 8 MiB; two were truncated and
one had partial/oversized lines. No raw records, account identifiers or commands were
copied into project records. No auth file, live account RPC, configuration or
ledger was read or created.

The Maintainer then named Antigravity as another required tool. A read-only
workspace-index query identified Cairn conversations without reading titles,
previews, summaries or search bodies. The immutable database base was used to
avoid state writes; its WAL was not included, so it is not a complete live
index. Three associated transcript samples, capped at 8 MiB each, exposed step
metadata but no counters in the inspected usage-field shapes. Two of those
samples were complete and one was truncated. The first three records of one
full transcript exposed the same field types. This is bounded evidence, not a
claim that Antigravity never records usage. No content values or binary
conversation data were inspected. Antigravity remains an explicit unknown
usage source, not an omitted tool or a zero-cost contributor.

Both token/cache shapes above occur in the samples. Codex also persists
`item_completed` records containing a `CommandExecution` item and integer
start/end times. The sampled command arrays were shell wrappers: this proves
command timing persistence, not reliable pytest classification. A synthetic
record using those field names and endpoints 1000/3500 represents 2.5 seconds;
it is not a private log excerpt. JUnit remains an independent test-time input.

No sampled usage/limit shape supplied the required spending account and
observation-time binding; creation-account metadata is not that proof. This is
a bounded observation, not a claim about every log or provider. The current
[official account documentation](https://developers.openai.com/codex/app-server)
describes authenticated live reads, not proof of those fields in persisted
logs. Consent is no longer the blocker. The remaining source-binding contract,
per-work attribution, implementation and empirical comparisons remain open;
there is no cost report or functioning budget stop yet.

**Elapsed**: approximately 15 minutes, including source inspection and writing.
**Tokens**: unknown. No suite, ongoing collection or private trial ran.

## Maintainer scope disposition -- Luna LOW -- 2026-11-05

**Authority**: Maintainer chat, 2026-11-05. This is scope approval only; it
does not change plan status, complete implementation, satisfy a review or
check, authorize activation, or grant another review pass.

> Okay, move the budget guard and unattended loop to v0.8. Update the plan and PLANNING board, and let's get measurement and reporting moving for v0.7. I don't want the planning/proposal docs for this left over, so please make a new v0.8 proposal be part of closing out this plan.

**Disposition**: Move the automatic account-bound between-item budget guard
and conditional unattended loop to v0.8. For v0.7, measurement and reporting
for all three tools and advisory A-C remain in scope. No accepted privacy,
accuracy, required-trial, or retirement check is waived; no unmetered automatic
launcher is authorized.

**v0.8 handoff**: Before either v0.7 plan archives, write one current joint
v0.8 proposal for the deferred guard and loop and link it from both v0.7 plans.
The archived v0.7 source proposals remain unchanged. Review, Decision, and
implementation of the v0.8 proposal are not completion criteria for these
v0.7 plans.

**Plan handling**: The meter plan's operative contract has not begun; Parent
High revises that contract before implementation. This record does not itself
complete or authorize implementation of the remaining v0.7 work.

## Author response -- Codex Sol (HIGH) -- 2026-11-05

The Maintainer's scope disposition is folded into the operative contract, not
left only in this response. The v0.8 proposal exists at `1e93a0de`.

- **Ordinary 1 / MSP1:** the unresolved account-at-observation/freshness proof
  now belongs to the deferred guard. v0.7 counts only supported source fields,
  preserves unknown account identity and refuses an unprovable requested account
  filter; it cannot promote a configuration label into provider evidence.
  Explicit root/project opt-in still controls every private read. The observed
  Codex timing shape is specified; shell-wrapped pytest classification and
  unsupported Antigravity usage remain unknown, not invented zero.
- **Ordinary 2-3 / MSP2-MSP3:** delivery, closed private retention, durable
  claim mapping and refresh-before-prune remain unchanged. C3 starts with public
  JUnit reporting independently of private collection, then joins C2's project
  aggregates. There is no spending-policy dependency or automatic launcher.
- **C4 remains required:** seven-day comparison, independent `ccusage` smoke,
  privacy and numerical checks, conditional Tokens retirement and Elapsed
  equivalence are not waived by the scheduling change. Inspection consent is
  not ongoing opt-in. Missing evidence still prevents their completion.
- **Closeout:** both current plans must leave a current joint v0.8 proposal
  with the complete deferred scope, source gaps and safeguards. They do not
  wait for that proposal's later review, Decision, guard or loop implementation.

No new clearing review is requested. This fold changes no runtime or trust
record; the ready-to-implement transition follows separately. Low-tier work
uses synthetic/public inputs; actual private-data work stays High and gated.

**Elapsed**: approximately 15 minutes. **Tokens**: unknown.

## Implementation log -- C3 public reporting checkpoint -- Codex Sol (HIGH) -- 2026-11-05

Source `46d39ef6` delivers the public JUnit slice, not all of C3. Luna executed
the reviewed contract; High author-side integration corrected `--json` routing
before publication. This was not an independent code or Security Review.
The source commit names the five changed paths, including CHANGELOG.
`gauge --pulse` reads only explicit reports, separates phase and session seconds,
reports case records rather than unique tests, and leaves all three tools'
usage unknown. No private collection or automatic admission is enabled.

**Boundary A -- Python 3.13.13.** On clean committed `46d39ef6` in a separate
Git-backed copy, select:

```sh
/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py for CHANGELOG.md dev/measurement/README.md tools/gauge.py tools/test_tiers.json bootstrap/tests/test_gauge.py
```

`python3.13 -m pytest -q --durations=0` with those 31 emitted paths and
`--junitxml=/private/tmp/cairn-meter-mapped-a.xml` yielded 1,757 passed,
14 failed, zero skipped: 1,771 nodes, 128.65 seconds wall. All failures
stopped at the portable-sweep fixture's denied `127.0.0.1` listener bind.
After inspecting that code, retry only those 14 failing node IDs with the local
listener permitted, the same interpreter and unchanged commit, using
`--junitxml=/private/tmp/cairn-meter-mapped-a-loopback-retry.xml`: 14 passed,
6.62 seconds pytest / 7.24 seconds wall. Every selected node passed across
the two attempts; the first attempt was not green. Clean pre/post state was
retained. No full-suite override, source repair or unrelated rerun was used.

The focused author check passed 27 cases, 14 deselected, in 0.94 seconds on
the byte-identical corrected reporting files. It includes JSON/Git routing,
malicious XML and file-shape refusals, and the no-Git CLI sentinel.
Claim, content, snippet, neutrality, redundancy, tier and diff checks passed;
three external links were not probed. Four over-10-second file observations
are in the consolidation plan; the 30-second iteration target was missed.

**Existing-report smoke.** `gauge --pulse --json --junit-report` with
`/private/tmp/cairn-c1-finalfix-ed6f1136.xml` reported 1,369 passed case records,
360.477 testcase phase seconds and 362.484 testsuite session seconds.
Missing seed kept comparability unknown. This parsed an existing report,
not a new test run or certification; no private source was inspected.

**Still open:** C1/C2, remaining C3 metrics/usage join, C4 real comparisons and
conditional retirement, ordinary and separate Security code reviews, and final
wide Boundary B. The joint v0.8 proposal is current through `c10b8491`; both
plans and the board link it without waiting for its future Decision.
Status remains `implementing`.

**Elapsed**: 135.89 seconds wall for mapped A plus its targeted retry;
overall checkpoint elapsed unknown. **Tokens**: unknown.

## Implementation log -- C1 source-to-project blocker -- Codex (gpt-6-luna, LOW) -- 2026-11-05

No collector code was changed. The reviewed C1 contract requires each source
project identity to map only to an allowlisted local project and then requires
comparison with that project's credential-stripped Git remote (C1, paragraph
beginning "Map source project identity"). The supported reader shapes in this
plan do not identify a project: Claude's listed assistant fields contain no
project field; Codex's listed `turn_context` use is only for model; Antigravity
content is explicitly not to be inspected. Assigning a configured root to a
project would make configuration a substitute for source evidence, while
reading an unlisted source field would widen the reviewed reader contract.

This needs a High-tier clarification of which supported source evidence binds
each record to an allowlisted project, or an explicit disposition for records
without that evidence. Until then, collection cannot safely produce
project-specific aggregates and C1 remains open. No host configuration,
logs,
private data, project data, or private trial were read. No guard, launcher,
trust record, baseline, or Security Review was run or changed.

**Covered**: C1 privacy/policy text and all three accepted reader-shape rows;
existing file/display and install-mapping patterns were inspected. **Not
covered**: implementation, tests, private sources/configuration, or any
Security Review. No tests ran; no implementation verification is claimed.

**Elapsed**: approximately 1 minute. **Tokens**: unknown.

## Author-side attribution evidence -- Codex Sol (HIGH) -- 2026-11-05

**Conclusion:** `d5385943` is narrowed, not cleared. Public metadata provides
identity candidates, not an unconditional session-wide project binding. This
is design clarification, not Security Review, a Decision, reader expansion or private
opt-in. C1/C2, C4 comparisons and conditional retirement remain owed; public
C3 reporting stays independent.

**Public evidence, not host observations:**

- **Claude:** [producer documentation](https://code.claude.com/docs/en/sessions#where-transcripts-are-stored)
  specifies the encoded working-directory folder, but permits a custom project
  directory name. [Cross-host resume](https://code.claude.com/docs/en/agent-sdk/sessions#resume-across-hosts)
  permits restoring a transcript under another project directory. The official
  [SDK reader](https://github.com/anthropics/claude-agent-sdk-python/blob/3be907edb9c86269d30d1427a77937dd788d6419/src/claude_agent_sdk/_internal/sessions.py)
  extracts `cwd` from the file head, otherwise substitutes its `project_path`
  argument; `gitBranch` is not a remote. These establish neither `cwd` on every
  usage-bearing assistant record nor its binding across resume. Hook
  `session_id`/`cwd`/`transcript_path` describe a different transport, not a
  persisted usage contract. Folder decoding or SDK fallback cannot supply proof.
- **Codex:** pinned [protocol](https://github.com/openai/codex/blob/49f0c6022596c361fe676a5c4738fb2be34e3a93/codex-rs/protocol/src/protocol.rs)
  defines `session_meta.payload.{id,session_id,cwd,git.repository_url}` and
  `turn_context.payload.{turn_id,cwd}`; the remote is optional. The
  [recorder](https://github.com/openai/codex/blob/49f0c6022596c361fe676a5c4738fb2be34e3a93/codex-rs/rollout/src/recorder.rs)
  collects Git information when writing initial metadata; resume appends with
  no new initial metadata. Its first metadata record identifies the owning
  thread; later headers can be copied fork history. The protocol accumulates
  `info.total_token_usage`; `event_msg.payload.type=token_count` supplies no
  project/turn identity in that payload. [Per-turn cwd overrides](https://developers.openai.com/codex/app-server)
  defeat assigning all cumulative usage to either initial or latest cwd.
  Matching an owned turn context to usage deltas is a candidate design, not a
  validated binding here; copied history and inherited checkpoints still need
  the accepted reconciliation proof.
  A stronger public candidate exists: the
  [response writer](https://github.com/openai/codex/blob/49f0c6022596c361fe676a5c4738fb2be34e3a93/codex-rs/core/src/session/mod.rs)
  persists `TokenUsageRecord` with `thread_id`, `turn_id`, `session_id`,
  `root_turn_id`, `response_id`, `usage`, `turn_token_usage` and
  `thread_token_usage`; it also persists turn contexts. The
  [persistence policy](https://github.com/openai/codex/blob/49f0c6022596c361fe676a5c4738fb2be34e3a93/codex-rs/rollout/src/policy.rs)
  retains this record. These bind response usage to producer IDs, not directly
  to a Git remote. Joining owned turn contexts is still required. This is a
  different shape from the accepted `token_count` row, not authority to add it.
- **Antigravity:** [status-line documentation](https://antigravity.google/docs/cli/statusline/)
  exposes `conversation_id`/`session_id`, `cwd`,
  `workspace.{current_dir,project_dir}`, and `context_window` counters together
  in a live payload. It establishes neither those fields in the accepted
  transcript shape nor historical project ownership of resumed cumulative
  counters. No capture/configuration change follows; persisted usage stays unknown.

**Synthetic evidence:** Python 3.13.13 ran nine checks: the
actual public SDK's isolated pure path encoder maps `/synthetic/repo-a` and
`/synthetic/repo/a` identically; eight constructed assertions cover moved copies,
100 then 130 across projects (new contribution 30), indistinguishable final-total
splits, foreign fork headers, conflicting duplicate identities, live versus
persisted shapes, a response-to-turn join and copied response keys. These are
counterexamples/candidate controls, not producer execution or collector
validation. No suite or actual-source test ran.

**Recommendation:** retain unknown/unattributed coverage, never guessed
project exports. A configured root authorizes no identity inference. Next,
specify and falsify a version-pinned Codex response-to-owned-turn binding using
the public writer and synthetic fixtures, comparing the direct response records
with the legacy checkpoint route. Include resume, fork/replay, missing context,
remote mismatches and conflicting copies. This may enable a supported subset;
it does not deliver Claude/Antigravity attribution or waive any accepted outcome.
Additional extraction outside the reviewed contract needs explicit disposition,
not a claim that all collection is ready. No new private inspection is needed
for this next step. No paths/cwd values from actual sources were read or retained.

**Author checks:** Python 3.13.13: claim, content/link integrity and snippet
checks passed; 17 external links were not probed by the prose gate. The tier
selector emitted zero test files; a direct-reader search found none, with a
known-positive gauge reader confirming the search. Neutrality is N/A: the gate's
named roots exclude `dev/`. No runtime files changed, collection enabled,
private logs/configuration read, private trial, full suite, push or trust
operation performed. Public source versions are not this host's verified versions.

**Elapsed**: unknown. **Tokens**: unknown.

## C1 implementation checkpoint -- Codex GPT-6 Luna (Low) -- 2026-11-06

The synthetic safety foundation is committed at `280543e177369f2eb98ea7b3a126bc47efcc801d`; its pre-meter upgrade fixture correction is `25172ab17e6839559f258cdad6e9017f6b3c7adb`, unsupported-platform hardening is `2cea4dfcca4f0160ff2df31459da420654df680e`, and no-follow config-path traversal is `6eb9cb1db79fbbdc5d5e0eb9445870ead7bac7a4`. The verbatim tools/template pair, closed versioned opt-in schema, POSIX private-config checks, and synthetic approved-root safe reader are in place. Missing or disabled configuration reports disabled. Invalid configuration and valid enabled configuration report unavailable; enabled configuration stops before source enumeration or ledger access. Reader identity and ownership coverage remain unknown. No collector, project binding, accounting identity, ledger, export, or private trial is delivered.

**Iteration evidence**: On clean commit `280543e177369f2eb98ea7b3a126bc47efcc801d`, Python 3.13.13 at `/Users/kendal30/conda_envs/lhm/bin/python3.13` ran the four focused owners `bootstrap/tests/integration/test_meter.py`, `bootstrap/tests/test_skills_install.py`, `bootstrap/tests/test_skills_upgrade.py`, and `bootstrap/tests/test_notice_install.py`: 166 passed and 4 failed in 3.53s. All four failures had the same cause: the simulated pre-meter adopter left `tools/meter.py` on disk after removing it from its lockfile. Commit `25172ab17e6839559f258cdad6e9017f6b3c7adb` corrects that fixture; rerunning its affected owner on a clean copy under the same interpreter produced 11 passed in 2.33s. After platform-fallback and optional-filter falsifiers were added, the same four owners on clean commit `2cea4dfcca4f0160ff2df31459da420654df680e` passed: 173 passed in 3.44s. After changing config reads to held no-follow directory descriptors, the same four owners on clean commit `6eb9cb1db79fbbdc5d5e0eb9445870ead7bac7a4` passed: 173 passed in 3.36s; its neutrality gate had zero failures and 43 informational findings. The first run's failures remain recorded; the corrected fixture and final focused selection pass. The source-code and shipped-file selector command listed 69 test files; only the four synthetic/install/count owners were run here. Ten POSIX-only test functions produce 11 platform-specific IDs; their independent High classification and transfer to the descriptor commit are recorded in the strict plan at `45b071c9` and `70abbb92`. The registry update remains root-owned and pending. The combined 69-file mapped selection remains due.

**Boundary B**: Not run. The final mapped integration selection remains due after ordinary and Security code review. The four focused owners are iteration evidence only.

**Known omissions**: Windows privacy evidence fails closed and was not tested on Windows. Source and project identity, ownership, source enumeration, accounting, ledger persistence, handoff integration, pulse join, comparisons, conditional Tokens retirement, and C2-C4 remain open. No private source, configuration, account, ledger, host log, or actual trial was read. No full suite, release operation, or re-anchor ran.
