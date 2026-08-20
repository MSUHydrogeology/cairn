<!-- Forward-reference paths this plan creates; they materialize in Chunks 5 and 7. -->

# Plan: measure structural events, not prose

**Source proposal**: [`dev/proposals/archive/2026-08-11-claude-metrics-events-not-prose.md`](../proposals/archive/2026-08-11-claude-metrics-events-not-prose.md)
**Status**: awaiting-plan-review
**Plan review**: required(External)
**Last update**: 2026-08-20
**Opened**: 2026-08-20

## Why this plan's review tier is External, not inherited

The source proposal's own header declares `**Plan review**: required(External) —
this changes the emitted schema of a **default-on** module, which every adopter
installs`, and that declaration is carried forward verbatim rather than
re-derived. This plan does **not** carry an `Inherited proposal basis:` field:
inheritance reallocates a plan review that would otherwise default to Internal,
and an External escalation is not eligible for that reallocation — pairing the
two is the incoherent combination the plan template's doctrine refuses. A
fresh-context Internal read is not a substitute here regardless of how settled
the seven review rounds below made the design: the module this plan ships is
installed by every adopter except the smallest, and its output schema is a
contract those adopters may already be parsing.

**Consequence for routing.** External review means a different agent type from
the implementer, or a human — no same-type sub-agent of the implementing agent
satisfies it. This plan sits at `awaiting-plan-review` until the Maintainer
routes it to a reviewer meeting that floor.

## Source proposal

`2026-08-11-claude-metrics-events-not-prose` went through seven Response/Revised
rounds and five External reviews (two agent identities: Antigravity ACCEPT,
Codex REVISE ×4) before the Maintainer accepted Round 7 on 2026-08-12. The
accepted contract has three parts. **Part 1** retires eight prose-scraped
columns (`total_findings`, `findings_p1/p2/p3`, four `review_yield_*`) from
routine emission, and the machinery that produces them, because a metric
derived by parsing review prose rewards writing more of it — the cheapest way
to look thorough is to split one finding into three. **Part 2** states the
selection principle in the module's own doctrine, next to the Measurement
Compact, and describes the columns Part 1 keeps honestly rather than as
immune to the same defect. **Part 3** replaces prose-parsing for the retained
event-shaped fields (`review_rounds`, reviewer identity/tier, `response_models`,
the stage-timing columns) with a closed-schema HTML-comment block appended to
the transitioning artifact by the same edit that performs the act, read back by
a rename-aware Git history algorithm that refuses — rather than silently
degrades — on any block it cannot reconcile to exactly one lifecycle act. This
plan executes that decision; it does not re-litigate any of the seven rounds
that produced it.

## Proposed paths

Proposed paths:
- `tools/_lifecycle_metrics/events.py` — the event-v1 grammar, history-diff reader, and reconciliation logic (Chunk 5); its `templates/` twin lands the same commit.
- `templates/modules/default-on/_lifecycle_metrics/events.py` — the gate-frozen twin of the above.
- `bootstrap/tests/test_lifecycle_metrics_events.py` — the new fixture file for the grammar/algorithm/reconciliation red and green cases (Chunks 4-7).

## Scope

**In, per the Decision:** all three parts, unabridged — retirement of the eight
columns and their full dependency graph (not just the CSV keys); the v2 schema
identity that makes the break machine-readable; the doctrine statement and the
honest re-description of the retained columns; the event-v1 grammar; the
rename-aware history-diff reader; fail-closed reconciliation on read; and
wiring every retained event-derived field to exactly one event kind. Nothing
here narrows any of Round 7's commitments — this is decomposition into
commits, not a second design pass.

**Out, by the Decision's own allowance — stated here, not silently restored.**
Historical continuity across the activation boundary is **dropped**: no
`--backfill` mode ships, no frozen historical snapshot is taken, and no
prose-derived value is substituted for a pre-activation artifact's event-shaped
fields. `Scope delta: degraded`, already authorized —

> "Drop historical continuity" — Anthony Kendall (Maintainer), Decision, 2026-08-12.

Chunk 6 states the concrete emission of this rule (what a pre-activation row
looks like) precisely so the allowance is not quietly reinterpreted at
implementation as "keep computing the old way until enough history exists."

**Out, because Round 5 explicitly removed it and no later round restored it —
flagged as a discrepancy from this task's own briefing, see "A correction to
this plan's own brief" below.** `tools/lifecycle.py` and its twin
`templates/skills/_lib/lifecycle.py` are **not touched by this plan.** They
belonged to the shared-ledger writer design that R3-E1 falsified and Round 5
abandoned outright ("No longer touched: `tools/lifecycle.py` and its twin... Both
belonged to the abandoned shared-ledger design" — Round 5, "Corrected
inventory"). The final architecture (Round 7) has no separate writer process at
all: the event block is written by the same edit that performs the act, and the
reader is the extractor. No chunk below touches `tools/lifecycle.py`.

**Out, unaffected:** `review-efficient-lifecycle`'s pilot-event ledger
(`dev/measurement/pilot-events.md`, `tools/lifecycle.py pilot-record` /
`pilot-report`). Round 5 explains why the two are separate files under one
writer-safety posture rather than one shared ledger: the pilot ledger is bounded
(retires at the end of its six-plan/60-day window) and lifecycle-metric events
are permanent, so mixing them gives the wrong lifetime to both. This plan does
not read, write, or extend that ledger.

### A correction to this plan's own brief

This plan was opened from a briefing that listed `templates/modules/default-on/_lifecycle_metrics/`
+ its `tools/` twin, **and** `tools/lifecycle.py` + its twin, as the Touches set
to carry forward. That listing matches the *proposal's original, never-revised
header* (`**Touches**:` line, top of the source proposal) — but the header is
stale. Round 5's "Corrected inventory" section explicitly supersedes it,
Round 6 adds `docs/glossary.md`, and neither Round 6 nor Round 7 (the operative
contract) touches `tools/lifecycle.py` again. Per this task's own instruction to
read Round 7 as the contract and treat earlier rounds as superseded history,
this plan follows the corrected inventory, not the stale header. Flagged
explicitly rather than silently resolved — see the report accompanying this
plan's opening commit.

### Documentation / doctrine surface

* `templates/modules/default-on/lifecycle-metrics.md` — module doctrine: removes
  the "finding severities" capability claim (two locations), adds the selection
  principle beside the Measurement Compact, reworks or bounds-marks the
  late-blocker section, and describes the retained columns as interim
  lifecycle proxies rather than inflation-immune (Chunk 2).
* `dev/agent_collaboration.md` and `templates/core/dev/agent_collaboration.md`
  — both carry the same "finding severities" phrase inside the
  `<!-- cairn:slot lifecycle-metrics -->` block, which the scaffold's own
  slot-merge machinery (`bootstrap/_scaffold/slotmerge.py`) derives from the
  module doc's "Template content" quote block. **This is a generated slot, not
  hand-authored prose** — the plan template's doc-tooling taxonomy applies:
  update the module-doc source, then re-render the slot via the scaffold's own
  merge path (Chunk 2 names the exact command it verifies).
* `docs/glossary.md` — sharpens the unconditional "never mine it for metrics"
  sentence under **Archive**, per R4-E3/Round 6's disposition, to distinguish a
  closed-schema block emitted *at* the transition from retrospective mining of
  prose it was never designed to carry (Chunk 2).
* `dev/proposals/_template.md`, `templates/core/dev/proposals/_template.md`,
  `dev/plans/_template.md`, `templates/core/dev/plans/_template.md` — the four
  activation-marker paths (Chunk 4). **Not a byte-identical twin pair** — the
  self-hosted copies already diverge from the shipped copies today (confirmed
  by diff: the self-hosted files carry Cairn's own filled content where the
  shipped files carry adopter fill-in slots and merge-block placeholders). Each
  of the four independently needs to carry the literal `cairn-event-v1` token;
  Round 7 §4 is explicit that Cairn and an adopter "each derive their own cutoff
  from their own history" — there is no shared constant to keep in sync.
* `CHANGELOG.md > Unreleased > Changed` — the v1→v2 schema break and the new
  event-emission convention (Chunk 8).
* No file under `doctrine/` — this plan executes an already-accepted design; it
  proposes no new cross-project doctrine beyond what the module and glossary
  already own.

## Sequence

```
1. Retire the eight columns and their dependency graph        [commit pending]
2. Doctrine: the principle, the honest description, the glossary sharpen [commit pending]
3. Version the break: v2 schema identity                      [commit pending]
4. Event-v1 grammar, the four activation markers, scaffold-only planner surfacing [commit pending]
5. The history-diff reader: identity, mutation detection, activation cutoff [commit pending]
6. Fail-closed reconciliation and wiring the retained fields  [commit pending]
7. Cross-cutting fixtures and the pre-existing-test audit     [commit pending]
8. CHANGELOG, manifest re-derivation, corpus before/after evidence [commit pending]
9. MAINTAINER-GATED — differential-oracle gate re-anchor ceremony [not performed by the implementing agent]
```

Chunks 1-3 have no dependency on Chunks 4-6 and may land in either order
relative to them; they are sequenced first here because Part 1/2 were stable
since Round 1 while Part 3 went through four more architectures. Chunks 4→5→6
are strictly ordered (grammar before reader before reconciliation). Chunk 7
depends on 1-6 all being present to exercise cross-cutting behavior. Chunk 8 is
bookkeeping and can land last. Chunk 9 is not part of this plan's own commit
sequence — see "The re-anchor ceremony" below.

### Chunk 1 — Retire the eight columns and their dependency graph

Confirmed by reading the live source (`tools/_lifecycle_metrics/`, as_of
2026-08-20): `total_findings`/`findings_p1/p2/p3` are computed at
`extract.py`'s finding-bullet loop (using `_FINDING_BULLET_RE` /
`_BRACKET_INTERIOR_RE`, imported from `parse.py`, with **no other consumer** —
verified by grep); the four `review_yield_*` columns come from
`subsystems._review_yield_counts`, whose entire supporting chain
(`_DISPOSITION_BUCKETS`, `_DISPOSITION_BULLET_RE`, `_normalize_disposition_token`,
`_parse_disposition_tokens`) has **no consumer besides `_review_yield_counts`
itself** — also verified by grep, so the whole chain is dead code once the
call at `extract.py` is removed, not just the four dict keys. `snapshot.py`'s
`METRIC_CONTRACT_MAP` carries exactly three review-yield entries
(`proposal_review_yield_accept_count`, `proposal_review_yield_reject_count`,
`proposal_review_yield_defer_count`).

| # | File | Change |
|---|------|--------|
| 1-1 | `tools/_lifecycle_metrics/extract.py` | Remove the `total_findings`/`findings` computation block and its four keys from the row dict; remove the `_review_yield_counts` call and its four keys; remove the now-dead `_FINDING_BULLET_RE`/`_BRACKET_INTERIOR_RE` import if `parse.py`'s audit (1-3) confirms no other consumer. Remove the eight names from `PROPOSAL_COLUMNS`. |
| 1-2 | `tools/_lifecycle_metrics/subsystems.py` | Remove `_review_yield_counts`, `_DISPOSITION_BUCKETS`, `_DISPOSITION_BULLET_RE`, `_normalize_disposition_token`, `_parse_disposition_tokens` — the whole review-yield chain, confirmed to have no other consumer. |
| 1-3 | `tools/_lifecycle_metrics/parse.py` | Remove `_FINDING_BULLET_RE`, `_BRACKET_INTERIOR_RE` once 1-1 confirms they have no remaining consumer. |
| 1-4 | `tools/_lifecycle_metrics/snapshot.py` | Remove the three `proposal_review_yield_*` entries from `METRIC_CONTRACT_MAP`. |
| 1-5 | `templates/modules/default-on/_lifecycle_metrics/{extract,subsystems,parse,snapshot}.py` | Identical edits, same commit — gate-frozen twin of 1-1..1-4. |
| 1-6 | `tools/lifecycle_metrics.py`, `templates/modules/default-on/lifecycle_metrics.py` | No source edit expected (thin launcher re-exports whatever the engine defines) — confirm unchanged, same commit as the twin above regardless. |
| 1-7 | `bootstrap/tests/test_reference_scripts.py` | `TestLifecycleMetricsSchema.test_installed_lifecycle_metrics_runs_on_target` (as_of 2026-08-20, lines 277-295): remove the `total_findings`/`findings_p1` assertions. Leave the `review_rounds` assertion as-is here — Part 3 has not landed yet at this point in the sequence, so `review_rounds` is still the pre-Part-3 heading count and the assertion still holds; Chunk 7 revisits this same test once Part 3 changes what computes that field. |
| 1-8 | `bootstrap/tests/test_lifecycle_metrics_config.py` | New or extended case: `PROPOSAL_COLUMNS` has exactly 22 entries (30 minus the eight retired, `as_of 2026-08-20` — re-derive at implementation, do not carry this count forward) and none of the eight retired names appear; every remaining structural column from the pre-change list is still present, asserted by name so a future accidental drop of a *kept* column fails loudly. |

**Acceptance for this chunk**: a fresh extractor run over a fixture proposal
with review findings emits no `total_findings`/`findings_p*`/`review_yield_*`
keys in either CSV or `--format md` output, while every retained column is
present and unchanged in value from before this chunk.

### Chunk 2 — Doctrine: the principle, the honest description, the glossary sharpen

| # | File | Change |
|---|------|--------|
| 2-1 | `templates/modules/default-on/lifecycle-metrics.md` | Remove "finding severities" from the opening capability paragraph and from "Reference implementation" (two locations, as_of 2026-08-20). Add the selection principle — *measure structural events as they occur; a metric that rewards writing more is a defect to remove, not a signal to tune* — as a framing statement beside the five-commitment Measurement Compact. Rework "Late-blocker reduction" so its bundle rests on structural signals, or mark it explicitly as a bounded study distinct from standing instrumentation (the proposal leaves this choice open; record which one this chunk takes and why). Describe the retained columns as interim lifecycle proxies, materially harder to inflate than a finding count but not immune (Round 1's withdrawn "cannot be inflated" claim stays withdrawn) — until Chunk 6 replaces them with genuine events, at which point this sentence is revisited so it does not overclaim in the other direction. |
| 2-2 | `templates/core/dev/agent_collaboration.md`, `dev/agent_collaboration.md` | Re-render the `<!-- cairn:slot lifecycle-metrics -->` block from the updated module-doc source via the scaffold's own slot-merge path — do not hand-edit the two copies independently out of sync. Verified by: `bootstrap/_scaffold/slotmerge.py`'s `merge_module_into_slot`/`check_slot_fidelity` is the actual mechanism (confirmed present, as_of 2026-08-20); the implementing chunk names the exact invocation it ran (`bootstrap/scaffold.py upgrade` against Cairn's self-hosted tree, or the narrower slot-render entry point if one exists — check `bootstrap/UPGRADE.md` before assuming the CLI shape) so a reviewer can re-run it. |
| 2-3 | `docs/glossary.md` | Sharpen the **Archive** entry's "never mine it for metrics" sentence (line 37, as_of 2026-08-20) to distinguish a closed-schema `cairn-event-v1` block emitted *at* the transition, in the same edit, from retrospective parsing of prose the artifact was never designed to carry. The existing sentence stays the default rule; this adds the narrow, named exception rather than replacing the rule wholesale. |

**Acceptance for this chunk**: `grep -rn "finding severities" templates/modules/default-on/lifecycle-metrics.md dev/agent_collaboration.md templates/core/dev/agent_collaboration.md` returns nothing; `python scripts/check_cairn.py` passes (link/anchor/claim-path integrity across the touched docs); the glossary sentence names the exception without weakening the general rule for anything that is not a `cairn-event-v1` block.

### Chunk 3 — Version the break: v2 schema identity

Depends on Chunk 1 (the eight columns are already gone from `PROPOSAL_COLUMNS`
by the time this chunk assigns the new identity).

| # | File | Change |
|---|------|--------|
| 3-1 | `tools/_lifecycle_metrics/snapshot.py` | Add a schema-version field to `output_manifest()`'s entries and to the persisted snapshot's own header/first row, distinguishing v2 (post-retirement) from v1 (pre-retirement, byte-preserved). Document the eight v1→v2 removals inline where the manifest already documents column lists. |
| 3-2 | `tools/_lifecycle_metrics/cli.py` | `--manifest` output (`format_manifest_md`) surfaces the version identity; no dual-emission path for the retired columns under any flag. |
| 3-3 | Twins under `templates/modules/default-on/_lifecycle_metrics/` | Identical edits, same commit. |
| 3-4 | `bootstrap/tests/test_lifecycle_metrics_config.py` or `test_reference_scripts.py` | A pre-existing (fixture-persisted) v1 snapshot's bytes are unchanged after this chunk lands; a freshly emitted snapshot carries the v2 identity and omits the eight columns; `--manifest` output names the version. |

**Acceptance for this chunk**: an adopter's pre-retirement snapshot file, present
in a fixture tree before this chunk's code runs, is byte-identical after it
runs (the tool never rewrites persisted output); a fresh run against the same
tree produces a new, v2-identified snapshot alongside it, never merged with or
overwriting the v1 one.

### Chunk 4 — Event-v1 grammar, the four activation markers, scaffold-only planner surfacing

Depends on nothing in Chunks 1-3. Independent of them; sequenced fourth because
it is the first Part-3 chunk and Chunks 5-6 depend on it.

The literal grammar, reproduced from Round 7 (not re-derived — this chunk pins
what Round 7 specified, it does not choose it):

```markdown
<!-- cairn-event-v1
kind: transition
from_state: reviewed
to_state: revised
-->
```
```markdown
<!-- cairn-event-v1
kind: review-pass
tier: External
reviewer: <reviewer name as written in the section heading>
-->
```
```markdown
<!-- cairn-event-v1
kind: response
model: <model identity as written in the Response's **Model** field>
-->
```

Closed key table (Round 7, reproduced verbatim as the binding contract for this
chunk):

| key | kinds | required | bounds |
|---|---|---|---|
| `kind` | all | yes | exactly one of `transition` / `review-pass` / `response` |
| `from_state`, `to_state` | `transition` | yes | a declared lifecycle status for that artifact type |
| `tier` | `review-pass` | yes | `Internal` / `External` / `Security` / `Code` |
| `reviewer` | `review-pass` | yes | ≤120 chars, single line |
| `model` | `response` | yes | ≤120 chars, single line |
| `recorded_by` | all | no | ≤120 chars; informational only — barred from authority, identity and idempotency |

Unknown key, unknown `kind`, unknown version token, missing required key, or a
value outside its bounds **refuses**, never ignores, never defaults. The
version token is the literal `cairn-event-v1`.

| # | File | Change |
|---|------|--------|
| 4-1 | `tools/_lifecycle_metrics/events.py` (new) | Grammar parser: recognizes the `cairn-event-v1` fence, validates the closed key table above, returns a typed block or a refusal reason. No history walking yet (that is Chunk 5) — this chunk is pure block-level validation. |
| 4-2 | `templates/modules/default-on/_lifecycle_metrics/events.py` (new) | Gate-frozen twin of 4-1, same commit. |
| 4-3 | `dev/proposals/_template.md`, `dev/plans/_template.md` | Add the literal `cairn-event-v1` marker — worked into the templates' own guidance for how an agent appends an event block at a transition, review pass, or response, so the marker is simultaneously the activation cutoff and the instruction a reader needs to act on it. |
| 4-4 | `templates/core/dev/proposals/_template.md`, `templates/core/dev/plans/_template.md` | The shipped equivalent. Independently must carry the literal marker; not required to be byte-identical to 4-3 (see Scope's "Documentation / doctrine surface" note on why these four paths are not a twin pair in the byte-identical sense). |
| 4-5 | `tools/lifecycle_planner.py`, twin `templates/skills/_lib/lifecycle_planner.py` | `next --to <state>`'s preview/mutation-manifest output additionally shows the literal event block the transitioning edit is expected to carry — scaffold-only, informational, not written to disk, not gating. The command's read-only contract is unchanged; a regression test confirms it still writes nothing (see 4-7). Not gate-frozen (outside `templates/modules/**`), but still a same-commit twin pair. |
| 4-6 | `bootstrap/tests/test_lifecycle_metrics_events.py` (new) | Grammar red/green fixtures: unknown key refuses; unknown `kind` refuses; unknown version token refuses; missing required key per kind refuses; a `reviewer`/`model` value over 120 chars refuses; the three worked examples above each parse cleanly. |
| 4-7 | `bootstrap/tests/test_lifecycle_contract.py` | Re-run (not necessarily re-write) the existing read-only regression — `test_every_subcommand_is_read_only` or its equivalent, as_of 2026-08-20 line 172 — against the extended preview output, confirming the new block-preview text changes stdout only, no byte written, no git operation performed. |

**Acceptance for this chunk**: every fixture in 4-6 passes; `next --to` remains
provably read-only under the existing contract test; the four template paths
each independently contain the literal string `cairn-event-v1`.

### Chunk 5 — The history-diff reader: identity, mutation detection, activation cutoff

Depends on Chunk 4 (the grammar it walks history to find).

The algorithm, reproduced from Round 7 §2-§4 as the binding contract:

1. Walk the artifact's rename-aware history, **oldest first**.
2. At each commit, parse the block sequence at that commit and at its parent;
   **the parent sequence must be an exact prefix of the child's** — any
   reordering, edit, or deletion of an existing block is a mutation and
   refuses.
3. Attribute only the added suffix to that commit.
4. Require the matching lifecycle act in the same diff (a `transition` block
   needs the `**Status**` change; a `review-pass` block needs the added review
   section; a `response` block needs the added Response section).
5. Refuse on ambiguous multi-parent attribution — a merge commit is never an
   introducing commit.

**Identity is `(introducing full commit SHA, added-block index)`**, both
derived by the algorithm above and never stored. Neither term names a path, so
the archive `git mv` cannot discontinue a series.

**Activation** is derived per marker path independently: the commit that first
adds the literal `cairn-event-v1` marker to the applicable *installed*
template in that tree (`dev/proposals/_template.md` for proposal-hosted
events, `dev/plans/_template.md` for plan-hosted events). Missing, divergent
(the pair disagrees), or multiply-introduced (removed and re-added) markers
refuse.

| # | File | Change |
|---|------|--------|
| 5-1 | `tools/_lifecycle_metrics/events.py` | History-diff walk (rename-aware, oldest-first), the parent-prefix mutation check, added-suffix attribution, matching-act requirement, multi-parent refusal, `(commit, index)` identity derivation, per-marker activation cutoff derivation. Reuses `gitmeta.py`'s existing git-subprocess pattern (`_git_log_for_path`, `--follow`) rather than a second implementation where that pattern already covers the need. |
| 5-2 | `templates/modules/default-on/_lifecycle_metrics/events.py` | Twin of 5-1, same commit. |
| 5-3 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Fixtures built against a real scratch git repository (reusing the `_git` helper pattern already present in `bootstrap/tests/test_lifecycle_contract.py`, as_of 2026-08-20 line ~70, rather than inventing a second one): a mutated (edited/reordered/deleted) existing block refuses; a merge commit introducing a block refuses; identity is stable before and after a `git mv` to `archive/`; missing, divergent, and multiply-introduced markers each refuse; a clean linear history with two distinct commits each adding one block resolves two distinct, stable identities. |

**Acceptance for this chunk**: every fixture in 5-3 passes against a real git
repository (not a mocked history), including the archive-rename identity
fixture, which is the concrete correctness case R5-E1 found broken in the
prior `(artifact path, block position)` identity scheme.

### Chunk 6 — Fail-closed reconciliation and wiring the retained fields

Depends on Chunk 5. This chunk is where Part 3 actually replaces prose-parsing
for the fields it claims, and where the `Scope delta: degraded` allowance gets
its concrete, checkable shape.

**The taxonomy (Round 6, reproduced as the binding contract):**

| Event kind | Emitted alongside | Retained fields it supplies |
|---|---|---|
| `transition` | the `**Status**` flip | transition dates; `days_*`, `hours_*`, `stage_timestamp_reliability`; `revised` |
| `review-pass` | each `## Review` / `## Plan review` / `## Code review` section | `review_rounds`, declared tier, `cross_agent_type_review`, reviewer identity |
| `response` | each `## Response` section | `response_models` |

**Fail-closed measurement on read.** The extractor is the canonical reader. It
exits nonzero `INCOMPLETE` when a post-activation event-bearing act has no
matching block, when a block has no matching act in its introducing commit, or
when reconciliation cannot be performed at all — including when Git itself is
unavailable for a post-activation artifact. This last case is a genuine
behavior change from today's tool, not explicit in the proposal text, and is
named plainly here rather than discovered at implementation: **the current
extractor runs without git** (`gitmeta.py`'s docstring: "Returns an empty list
when git is not available... a deliberately quiet failure mode"), degrading
silently to header-date-only reliability. Once an artifact's activation marker
exists and the artifact carries a status past that cutoff, this chunk makes
"no git available" a **refusal of that artifact's row**, not a quiet downgrade
— because "reconciliation cannot be performed at all" is exactly what
"unavailable Git" is. Chunk 7 audits every existing test that currently runs
this tool without a git-initialized scratch tree, because this is where their
assumptions break.

**The dropped-historical-continuity allowance, made concrete.** For an artifact
whose relevant act (transition / review-pass / response) predates that
artifact's own activation cutoff, the corresponding event-derived field is
emitted **empty** — not computed from the old prose-parsing path, not backfilled,
not marked "derived/unreliable" (both of those were the rejected option (b)).
Empty is the correct value per the Decision, not a placeholder for a future
backfill this plan does not build. Post-cutoff acts on the same artifact are
reconciled and refuse-on-mismatch exactly as above; an artifact can therefore
carry an empty `review_rounds` for its pre-cutoff review passes and a
populated one for later passes on the same document, and the reader must not
conflate the two into one silently-partial number.

| # | File | Change |
|---|------|--------|
| 6-1 | `tools/_lifecycle_metrics/events.py` | Reconciliation: per-artifact, per-kind matching of acts to blocks; `INCOMPLETE` disposition (nonzero exit, explicit reason) on any unmatched act, unmatched block, or unresolvable history (including unavailable Git for a post-activation artifact). |
| 6-2 | `tools/_lifecycle_metrics/extract.py` | Post-activation: `review_rounds`, reviewer identity/tier, `cross_agent_type_review`, `response_models` sourced from reconciled `review-pass`/`response` blocks, not from heading counts or `**Model**:` regex scraping. Pre-activation acts on the same artifact: the corresponding field is empty per the rule above. Transition dates / `days_*` / `hours_*` / `stage_timestamp_reliability` / `revised` sourced from reconciled `transition` blocks post-cutoff; unchanged (still header/git-timestamp-derived, still quiet-downgrade) pre-cutoff, since that is the existing degradation this chunk does not touch for the historical portion. |
| 6-3 | Twins under `templates/modules/default-on/_lifecycle_metrics/` | Same commit as 6-1/6-2. |
| 6-4 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Mandatory red fixtures (Round 6 / R4-E2): a status-only commit with no block → `INCOMPLETE`; a review-only commit with no block → `INCOMPLETE`. Mandatory taxonomy fixture (Round 6 / R4-E1): two review commits with no intervening status change produce **two** review-pass events and `review_rounds == 2`. Pre/post-activation split fixture: one artifact with a review pass before its activation cutoff and one after; the row shows an empty value attributable to the pre-cutoff pass and a populated, reconciled value for the post-cutoff one. |

**Acceptance for this chunk**: every fixture in 6-4 passes; a report run against
a fixture tree containing a deliberately unreconciled act exits nonzero and
names which artifact/commit/kind failed to reconcile, never a shorter clean
series.

### Chunk 7 — Cross-cutting fixtures and the pre-existing-test audit

Depends on Chunks 1-6 all being present.

| # | File | Change |
|---|------|--------|
| 7-1 | `bootstrap/tests/test_lifecycle_metrics_events.py` | Confirms cross-commit contamination is structurally unrepresentable (the R3-E1 property, re-expressed for the artifact-local design per Round 5 §2): two artifacts transitioned concurrently, one commit path-scoped to the first artifact only, and the assertion that the second artifact's block does not and cannot appear in that commit — because there is no shared file for it to appear in. This is a confirmation test of a structural property, not a vulnerability regression test (there is no longer a vulnerable mechanism to regress). |
| 7-2 | `bootstrap/tests/test_lifecycle_metrics_events.py` | `recorded_by` fixture: a block carrying a forged or duplicated `recorded_by` value changes no identity, no reconciliation outcome, and no refusal disposition — confirming it stays informational-only per Round 7's explicit bar on it participating in authority or idempotency. |
| 7-3 | `bootstrap/tests/test_reference_scripts.py` | `test_installed_lifecycle_metrics_runs_on_target` (as_of 2026-08-20, the same test Chunk 1 already touched): once Chunk 6 lands, this fixture's `tmp_path` has no `.git` at all. Reusing the git-init pattern already present in this same file (as_of 2026-08-20, around line 469) is one option; asserting the new `INCOMPLETE`-refusal path directly, once the fixture proposal is activation-eligible, is the other. This chunk decides which and updates the test so it keeps exercising what it is meant to exercise, rather than accidentally exercising the new refusal path by omission. |
| 7-4 | `bootstrap/tests/test_lifecycle_contract.py` | Confirm the corpus-soundness suite (`test_the_live_corpus_is_sound_under_the_p1_contract` and neighbors) still passes against Cairn's own live `dev/proposals/` and `dev/plans/` corpus once the four template paths carry the activation marker — the live corpus itself carries no event blocks yet (this plan does not backfill), so this is a check that adding the marker to the templates does not itself perturb anything the corpus-soundness suite reads. This file is also touched by two other proposals opening today (both editing `bootstrap/tests/conftest.py`); this plan does not touch `conftest.py` and has no other point of contact with that concurrent work. |

**Acceptance for this chunk**: 7-1 through 7-3 pass as new/updated fixtures; 7-4
is a confirming (not new) pass against the live corpus.

### Chunk 8 — CHANGELOG, manifest re-derivation, corpus before/after evidence

| # | File | Change |
|---|------|--------|
| 8-1 | `CHANGELOG.md > Unreleased > Changed` | One line naming the v1→v2 lifecycle-metrics schema break (eight columns retired) and the new event-emission convention for adopters who already parse the CSV/manifest. |
| 8-2 | *(evidence, not a file change)* | Re-run the extractor against Cairn's own corpus before and after this plan's chunks, diffing the emitted column set — the "Owed at implementation" item the proposal names explicitly, so the diff is recorded rather than assumed. Recorded in this plan's `## Implementation verification` section, not carried into the plan as a number now. |

## Sequence revision — the re-anchor ceremony

**MAINTAINER-GATED.** Chunks 1, 3, 4, 5, 6, and 7 modify files under
`templates/modules/**/*.py` and `bootstrap/tests/**/*.py`, both gate-frozen
surfaces under the differential-oracle gate. Landing any of them trips the gate
and requires the supervised re-anchor ceremony described in
`bootstrap/REANCHOR_RUNBOOK.md` (`bootstrap/reanchor.sh`) — Phase 0, Phase 4,
and Phase 5 of that ceremony are explicitly **not** performed by an implementing
agent (the "implementer blesses its own verifier" self-authorization the
runbook itself forbids). This plan does not perform the re-anchor; it names the
need and stops there.

**A second re-anchor is already owed, for an unrelated reason.**
`dev/PLANNING.md`'s Queued section (as_of 2026-08-20) carries a `[VER]` row: the
AST attestation baseline (`bootstrap/tests/test_ast_attest.py`, a *different*
trust root from the differential-oracle gate anchor, governing the
`bootstrap/_scaffold/` engine package specifically) needs re-anchoring after an
unrelated docstring pass, via `bootstrap/AST_BASELINE_RUNBOOK.md`, and that
repair is explicitly **not self-serviceable** by an implementing agent either.
This plan's changes do not touch `bootstrap/_scaffold/` and do not themselves
require the AST-baseline re-anchor. **Batching this plan's differential-oracle
gate re-anchor with that already-owed AST-baseline re-anchor into one Maintainer
ceremony is the shape that avoids running the Maintainer-only ceremony twice in
quick succession — presented here as an option for the Maintainer to choose,
not decided by this plan.**

## Acceptance criteria

* **Tests that must pass**: every fixture named in Chunks 1, 3, 4, 5, 6, and 7's
  file tables, by node once implemented; `bootstrap/tests/test_lifecycle_contract.py`
  unchanged in outcome (confirming pass, not a new fixture) except where 4-7 and
  7-4 name a specific extension.
* **Doc updates that must land**: `templates/modules/default-on/lifecycle-metrics.md`,
  `dev/agent_collaboration.md` + its shipped twin (re-rendered, not hand-edited),
  `docs/glossary.md`, the four activation-marker template paths, `CHANGELOG.md`.
* **Examples / smoke checks required**: `python scripts/check_cairn.py` (doc
  link/anchor/claim-path integrity across every touched Markdown file);
  `python tools/lifecycle_metrics.py --manifest` run against a scratch tree,
  confirming the v2 identity and the absence of the eight retired columns;
  `python tools/lifecycle_planner.py next <fixture> --to <state>` confirming the
  read-only contract under the extended preview text (4-7).
* Inbound path-link updates: none expected — `dev/PLANNING.md` and
  `dev/NEXT_SESSION.md` refer to plans by filename stem, not path link, so the
  archive-move needs no update there.

### Author-accounting — invariants, failure modes, edge cases

**Security preflight, re-answered against the actual accepted architecture.**
The source proposal's own security preflight went stale mid-deliberation: Round
2's preflight (lines 482-502) and Round 4's "corrected" preflight (lines
805-826) both describe the **shared-ledger** writer design that R3-E1 falsified
and Round 5 abandoned. **No round after Round 5 re-answered the five questions
against the artifact-local design that Round 7 actually specifies and the
Decision actually accepts.** This is a genuine gap in the record, named
explicitly rather than papered over; the five questions are re-answered here
for the first time against the real architecture:

1. **Untrusted input?** The event blocks are agent/human-authored text inside
   already-tracked, already-reviewed `dev/proposals/`/`dev/plans/` files — the
   same trust tier as the rest of the lifecycle corpus, not external input. It
   is nonetheless a real parsing surface (Chunk 4's closed key table, bounds,
   and refuse-on-unknown behavior is the containment).
2. **Executes anything?** No. The reader parses text and shells out to `git
   log`/`git diff` (the same subprocess pattern `gitmeta.py` already uses) —
   no execution of artifact content.
3. **Can it pass when it should fail?** This is the chunk-6 reconciliation
   contract's entire job: any malformed block, mutated block, unmatched act,
   or unresolvable history refuses rather than passing. The mandatory red
   fixtures in 4-6 and 6-4 are what pin this, not prose.
4. **Can it fail when it should pass?** Yes, by design and named as a known
   trade-off: a legitimate transition performed through an unusual git workflow
   (a squash, a history rewrite, a shallow clone) that the history-diff
   algorithm cannot attribute will refuse rather than guess. The cost is a
   loud `INCOMPLETE`, not a wrong number — the asymmetry this whole design
   exists to enforce.
5. **Widens a trust boundary?** No new trust boundary: no shared ledger, no new
   writer process, no file outside the already-tracked, already-reviewed
   artifact tree. `next --to`'s read-only guarantee is unchanged (4-7
   regression-tests this explicitly).

**Invariants and their enforcing tests** (test names are illustrative of the
property each pins, not final — the implementing chunk names them for what
they check, not for the round or finding that asked for them, per this
project's own naming convention):

| Invariant | Enforced by |
|---|---|
| The eight retired columns never appear in emitted output | Chunk 1's extension to `test_reference_scripts.py` + `test_lifecycle_metrics_config.py` |
| `_lifecycle_metrics/` and `lifecycle_metrics.py` twins stay byte-identical | the existing, already-passing `bootstrap/tests/test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source` — manifest-derived, already covers these two pairs; no new test needed, only commit discipline |
| v1 snapshot bytes are never rewritten by the v2 code path | Chunk 3's fixture |
| Unknown key / kind / version / missing-required / out-of-bounds each refuse | Chunk 4's grammar fixtures |
| An edited, reordered, or deleted existing block refuses (mutation) | Chunk 5's history fixture |
| A merge commit is never an introducing commit | Chunk 5's merge-commit fixture |
| Identity survives the archive `git mv` | Chunk 5's archive-rename fixture |
| Missing / divergent / multiply-introduced activation marker refuses | Chunk 5's marker fixtures |
| A status-only commit with no block is loud `INCOMPLETE` | Chunk 6's mandatory red fixture |
| A review-only commit with no block is loud `INCOMPLETE` | Chunk 6's mandatory red fixture |
| Two review commits, no intervening status change, yield two review-pass events | Chunk 6's mandatory taxonomy fixture |
| Pre-activation acts emit empty, not prose-derived, not backfilled | Chunk 6's pre/post-activation split fixture |
| Cross-commit contamination is structurally unrepresentable | Chunk 7's confirmation fixture |
| `recorded_by` never affects identity, reconciliation, or refusal | Chunk 7's fixture |
| `next --to` stays read-only under the extended preview | Chunk 4's and Chunk 7's regressions against `test_lifecycle_contract.py` |
| Unavailable Git on a post-activation artifact refuses the row, not a quiet downgrade | Chunk 6's reconciliation logic + Chunk 7's audit of `test_installed_lifecycle_metrics_runs_on_target` |

**Known omission, named rather than discovered later.** No test in this plan
exercises a shallow clone or a rewritten-history repository directly (Round
7's enumerated fail-closed dispositions include both). The implementing chunk
either adds fixtures for these two cases under Chunk 5 or records them as an
explicit residual in that chunk's own acceptance record — this plan does not
assume they are free to skip.

## Verification

Boundary A (iteration): the reviewed mapping is the fixture list in each
chunk's file table above, plus the standing gates for every touched surface —
`python scripts/check_cairn.py` for every Markdown change, `python
scripts/quality_gate.py --sub neutrality --sub redundancy` for every touched
template/doctrine file.

Boundary B (integration, after the final implementation commit): this plan
touches a **contract surface** — the emitted schema of a default-on module that
`bootstrap/fidelity-check.md` and `scaffold.py --manifest` both describe as
adopter-relied-upon — so **bounded mode refuses** and Boundary B runs the
**full suite**, per AGENTS.md's own refusal rule. No chunk here narrows that.

* `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`
* `python scripts/quality_gate.py --sub neutrality --sub redundancy`
* `python scripts/check_cairn.py`
* `python scripts/claim_check.py dev/plans/metrics-events-not-prose.md` (this
  file, at authoring time — already run before this commit, see below)
* Plan-specific: `python tools/lifecycle_metrics.py --manifest` against a
  scratch tree; `python tools/lifecycle_planner.py next <fixture> --to <state>`
  confirming the read-only contract; the extractor's before/after corpus
  column diff named in Chunk 8.

Append `## Implementation verification -- <agent> -- YYYY-MM-DD` after the
final implementation commit, per the plan template's exact-fields contract.

## Code review

*Filled in after implementation commits land.* See `doctrine/plans.md` >
"Code review" for the full doctrine — falsification ledger, coverage line,
reviewer identity (not the implementing agent), and the append-only rule.

## Lasting-truth migration

*Filled in at archive time.* See `doctrine/plans.md` > "Lasting-truth migration
doctrine."
