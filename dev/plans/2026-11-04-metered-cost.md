# Plan: Meter real cost without collecting conversations

**Source proposal**: dev/proposals/archive/2026-10-30-claude-metered-cost.md
**Author**: Sol (security/design plan author; high)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Measure opted-in agent usage privately, report team cost, and stop unattended work when a fresh spending reading cannot admit it.
**Elapsed**: 5m21s (17:26:08-17:31:29 UTC; finalization excluded)
**Tokens**: unknown

## Source proposal

The heavy Decision accepts the revised meter, weekly pulse, cooperative
unattended stop and conditional Tokens retirement; Elapsed stays until
equivalence. Operative text, MC1-MC3/MS1-MS2 response and Decision are preserved;
opening archives the source unchanged.

## Scope

Proposed paths:
- `tools/meter.py`
- `bootstrap/tests/test_meter.py`
- `bootstrap/tests/test_gauge.py`

One standard-library collector, `tools/meter.py`, with small tool readers
(tool-specific `vendor-ok` annotations),
private per-user configuration/ledger outside repositories and project-only
gitignored aggregates.
No proxy, daemon, dependency adoption, per-artifact agent targets or scores.
No host configuration, private-log access, signing or baseline change now.

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
Suite growth/runtime reuse batch 2a's existing records and tier map; no new store.

### Documentation / doctrine surface

Describe usage/privacy in `dev/measurement/README.md` and correct the outdated
measurement description in `docs/methodology/rationale.md`.
Admission rules touch `.agents/skills/session-start/SKILL.md` and
`templates/skills/session-start/SKILL.md`; handoff touches
`.agents/skills/session-end/SKILL.md`, `templates/skills/session-end/SKILL.md`
and byte-identical `tools/session.py`/`templates/skills/_lib/session.py`.
Conditional Tokens edits cover `dev/proposals/_template.md`,
`dev/plans/_template.md`, `templates/core/dev/proposals/_template.md` and
`templates/core/dev/plans/_template.md`; historical records remain intact.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Constrained collector and local configuration contract | Both plan reviews folded | Synthetic privacy/safety fixtures; disabled-by-default collector |
| C2 | Accounting, attribution and refresh | C1 | Incremental ledger, claim retention, handoff integration |
| C3 | Pulse and unattended admission | C2; 2a reporting interface | Gauge report, pre-item check and consumer tests |
| C4 | Executable comparisons and conditional template retirement | C1-C3; MAINTAINER-GATED actual private trial only | Agent-owned trial evidence and earned Tokens retirement |

Low-tier agents execute reviewed contracts on synthetic data; new
privacy/admission judgment returns to high. Private-data work never downshifts
across its governance boundary. Configuration/policy remain the Maintainer's
choice. On reaching missing opt-in, record the normal Waiting line, continue
independent preparation, then wait; neither
acceptance nor this opening chat supplies consent.

## Acceptance criteria

**C1.** Explicit local configuration allowlists source roots, accounts and
projects, identifying projects by credential-stripped remote. No auto-discovery
of unlisted projects. Reject links in ancestors/leaves, non-regular inputs,
oversized lines and non-finite/negative usage. Revalidate opened identity and
bounded reads; retain no prompt, response or command text. Retained fields are
usage, timestamps, model/account ids, classified test intervals and sanitized
project identity only. Strip remote userinfo, credential query/fragment and
SCP credentials before storage; ambiguous identity
is unknown. Private directories/files use restrictive permissions; atomic writes
refuse redirected destinations and preserve old bytes on failure. Project output
contains only its own aggregates. Secret/control-byte fixtures cover bodies,
remotes, filenames, stdout/stderr and failed writes: errors identify sanitized
file aliases/line numbers, never input or exception text; names use `encode_display`.

**C2.** Namespace/deduplicate message ids across repeated/rotated files; retain
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

**C3.** `tools/gauge.py --pulse` reports week/project/artifact usage and time,
test waits, review passes, model-tier mix, always-loaded cost and shared 2a suite
growth/runtime, with source/window/coverage. Count standalone review side-files
with parents; expose orphans/unspecified models. Distinguish metered tokens from
word/byte-derived estimates. Missing 2a evidence is unknown, not completed reporting.
Before every drain item, refresh then admit only a finite nonnegative reading
strictly below the configured limit, matching source/account/unit/reset-window
and maximum age. Policy limits/ages must also be finite and positive; age uses
source observation time, never refresh time. Missing policy, stale/future
timestamps, NaN, incomplete coverage, mismatch, refresh failure and exhausted
limits stop unattended admission; attended
work remains available. Units are named-window plan percent or weighted tokens/day,
never interchangeable. This cooperative check cannot authenticate mutable logs or
prevent one-item/concurrent-session overshoot; report those residuals explicitly.

**C4.** Implement `python tools/meter.py --trial record` and
`python tools/meter.py --trial check`, using explicit local configuration.
Test synthetically, then run agent-owned after root/project/account opt-in.
Over seven days, record weighted deltas and source plan-percent readings within matched reset
windows; increases must move together beyond source rounding resolution, with
resets/missing observations visible. Record ratios, resolution and counterexamples,
not a fabricated percent conversion. Run an independently installed `ccusage`
count smoke on the same approved logs/time range and reconcile each token kind
exactly; never install/adopt it as a Cairn dependency or silently fetch it.
Missing executable/percentage/access leaves this accepted check open. Trial
comparisons exit nonzero for disagreement/incomplete evidence and retain only
sanitized aggregates. Retire Tokens only after ALL meter checks, including both
real comparisons, pass. Keep Elapsed unless timestamp evidence demonstrates the
same elapsed quantity within source resolution; unknown equivalence means retain.

## Scope delta

**Scope delta**: preserved. No accepted test is converted to human paperwork or
silently deferred; missing consent/evidence keeps implementation open.

## Verification

Boundary A selects `python tools/test_tiers.py for <paths>` per chunk.
`bootstrap/tests/test_meter.py` owns ingestion/accounting/admission/trial
falsifiers; `bootstrap/tests/test_gauge.py` owns pulse grouping and 2a evidence.
Existing canonical homes:
`bootstrap/tests/test_session_start_drain_rules.py` (skill admission),
`bootstrap/tests/test_session_routines.py` and `bootstrap/tests/test_session_failsafe.py`
(handoff ordering/failure), `bootstrap/tests/test_session_writes_contained.py`
(file/display safety), `bootstrap/tests/test_intents_tool.py` (digest/prune
compatibility). Re-resolve homes after 2a moves; preserve node identity.
Exercise actual meter, pulse and handoff CLIs on synthetic roots; admission
fixtures must observe the next item not starting, not just a printed refusal.
S2 mutations belong to C1-C3 tests; S3 is their selected pytest invocation plus
the C4 trial commands. Removing a secret filter, freshness/unit check or dedup
must fail its owning test. Other S1/S4/S5 answers remain the accepted preflight.
Target the tiny meter module below one second; record runtime misses.

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
